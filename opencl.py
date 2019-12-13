#!/usr/bin/env python3
import time
import cv2
import numpy as np
import pyopencl as cl
from scipy import ndimage
import skimage.transform

def calc_fractal_numpy(chunks, maxiter):
    output_chunks = []

    for chunk_input in chunks:
      chunk_output = np.zeros(chunk_input.shape, dtype=np.uint16)

      z = np.zeros(chunk_input.shape, np.complex)

      for it in range(maxiter):
          z = z*z + chunk_input
          done = np.greater(abs(z), 2.0)
          chunk_input = np.where(done, 0+0j, chunk_input)
          z = np.where(done, 0+0j, z)
          chunk_output = np.where(done, it, chunk_output)

      output_chunks.append(chunk_output)

    return np.concatenate(output_chunks)

def calc_fractal_opencl(chunks, maxiter):
    # List all the stuff in this computer
    platforms = cl.get_platforms()

    for platform in platforms:
        print("Found a device: {}".format(str(platform)))

    # Let's just go with platform zero
    ctx = cl.Context(dev_type=cl.device_type.ALL,
                     properties=[(cl.context_properties.PLATFORM, platforms[0])])

    # Create a command queue on the platform (device = None means OpenCL picks a device for us)
    queue = cl.CommandQueue(ctx, device = None)

    mf = cl.mem_flags

    # This is our OpenCL kernel. It does a single point (OpenCL is responsible for mapping it across the points in a chunk)
    prg = cl.Program(ctx, """ 
    #pragma OPENCL EXTENSION cl_khr_byte_addressable_store : enable
    __kernel void mandelbrot(__global float2 *q, __global ushort *output, ushort const maxiter)
    {
      int gid = get_global_id(0);

      float cx = q[gid].x;
      float cy = q[gid].y;

      float x = 0.0f;
      float y = 0.0f;
      ushort its = 0;

      while (((x*x + y*y) < 4.0f) && (its < maxiter)) {
        float xtemp = x*x - y*y + cx;
        y = 2*x*y + cy;
        x = xtemp;
        its++;
      }

      if (its == maxiter) {
        output[gid] = 0;
      } else {
        output[gid] = its;
      }
    }
    """).build()

    output_chunks = []
    output_chunks_on_device = []

    chunk_shape = None

    for chunk_input in chunks:
        # Record the shape of input chunks
        chunk_shape = chunk_input.shape

        # These are our buffers to hold data on the device
        chunk_input_on_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=chunk_input)

        chunk_output_on_device = cl.Buffer(ctx, mf.WRITE_ONLY, int(chunk_input.nbytes / 4))
        # divided by 4 because our inputs are 64 bits but outputs are 16 bits

        # Call the kernel on this chunk
        prg.mandelbrot(queue, chunk_shape, None, chunk_input_on_device, chunk_output_on_device, np.uint16(maxiter))

        # Add the output chunk to our list to keep track of it
        output_chunks_on_device.append(chunk_output_on_device)

    # Wait for all the chunks to be computed
    queue.finish()

    for chunk_output_on_device in output_chunks_on_device:
        chunk_output = np.zeros(chunk_shape, dtype=np.uint16)

        # Wait until it is done and pull the data back
        cl.enqueue_copy(queue, chunk_output, chunk_output_on_device).wait()

        # Insert the chunk in our overall output
        output_chunks.append(chunk_output)

    return np.concatenate(output_chunks)

def apply_blur_opencl(image, radius, strength) :
    platforms = cl.get_platforms()

    ctx = cl.Context(dev_type=cl.device_type.ALL,
                     properties=[(cl.context_properties.PLATFORM, platforms[0])])

    queue = cl.CommandQueue(ctx, device = None)
    mf = cl.mem_flags

    image_dims = image.shape

    filt = np.ones((radius, radius), dtype=np.float)

    preamble = """
    #define IMAGE_W {}
    #define IMAGE_H {}
    #define FILTER_SIZE {}
    #define HALF_FILTER_SIZE {}
    #define STRENGTH {}
    """.format(image_dims[0], image_dims[1], int(radius), int(radius/2), int(strength))

    prg = cl.Program(ctx, preamble +
    """
    #pragma OPENCL EXTENSION cl_khr_byte_addressable_store : enable
    __kernel void convolve(const __global float *input,
                           __global float *output,
                           __constant float *filter) {

      int y = get_global_id(1);
      int x = get_global_id(0);

      if ( y > HALF_FILTER_SIZE && y < ((IMAGE_H - HALF_FILTER_SIZE) - 1) &&
           x > HALF_FILTER_SIZE && x < ((IMAGE_W - HALF_FILTER_SIZE) - 1)) {
        float sum = 0.0f;

        for (int ky = 0; ky < FILTER_SIZE; ky++) {
          for (int kx = 0; kx < FILTER_SIZE; kx++) {
            sum += input[(y * IMAGE_W) + (ky-HALF_FILTER_SIZE) + x + (kx-HALF_FILTER_SIZE)] *
                   filter[ky * FILTER_SIZE + kx];
          }
        }

        output[y * IMAGE_W + x] = sum / (float)STRENGTH;
      } else {
        output[y * IMAGE_W + x] = 0.0f;
      }
    }
    """).build()

    image_on_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=image)
    filter_on_device = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=filt)
    output_on_device = cl.Buffer(ctx, mf.WRITE_ONLY, image.nbytes)
    output = np.zeros(image_dims, dtype=np.float)

    prg.convolve(queue, image_dims, None, image_on_device, output_on_device, filter_on_device)

    cl.enqueue_copy(queue, output, output_on_device).wait()

    return output


if __name__ == '__main__':

    class Mandelbrot(object):
        def __init__(self):
            self.zoom = 1024
            self.centre_x = -(1.6*self.zoom)
            self.centre_y = 0
            self.w = 1920*4
            self.h = 1080*4
            self.w_range = 19.2
            self.h_range = 10.8
            self.iterations = 64
            self.chunks = 10
            self.fname = "mandelbrot.jpg"

            self.beautify = True
            # To get crisper edges, also throw out points with less than this number of iterations
            self.cutoff = 0.125 * self.iterations

            self.r_spread = 0.4
            self.g_spread = 0.4
            self.b_spread = 0.4

            self.render((self.centre_x-self.w_range)/self.zoom, (self.centre_x+self.w_range)/self.zoom,
                        (self.centre_y-self.h_range)/self.zoom, (self.centre_y+self.h_range)/self.zoom, self.iterations)
            self.save_image()

        def render(self, x1, x2, y1, y2, maxiter):
            # Create the input
            xx = np.arange(x1, x2, (x2-x1)/self.w)
            yy = np.arange(y2, y1, (y1-y2)/self.h) * 1j
            q = np.ravel(xx+yy[:, np.newaxis]).astype(np.complex64)

            # Slice the input up into chunks to be processed in parallel
            chunk_width = self.w
            chunk_height = self.h / self.chunks
            chunked_data = np.split(q, self.chunks)

            # Set up the output
            output = np.zeros_like(q)
            chunked_output = np.split(output, self.chunks)

            start_main = time.time()

            output = calc_fractal_opencl(chunked_data, maxiter)

            end_main = time.time()

            secs = end_main - start_main
            print("Main took", secs)

            self.mandel = output.reshape((self.h, self.w))

        def save_image(self):
            normalized = self.mandel.astype(np.double)
            normalized = (normalized / (normalized.max())) * 255.0
            normalized = np.clip(normalized - self.cutoff, 0, 255)

            b = normalized
            g = normalized
            r = normalized

            if (self.beautify):
              filtered = normalized
              b_filtered = ndimage.uniform_filter(filtered, size=int(11*self.b_spread))
              g_filtered = ndimage.uniform_filter(filtered, size=int(11*self.g_spread))
              r_filtered = ndimage.uniform_filter(filtered, size=int(11*self.r_spread))

              b_filtered_mean = b_filtered.mean()
              g_filtered_mean = g_filtered.mean()
              r_filtered_mean = r_filtered.mean()

              b = ((b_filtered / b_filtered_mean))
              g = ((g_filtered / g_filtered_mean))
              r = ((r_filtered / r_filtered_mean))

              # Renormalize
              b = (b / b.max()) * (255.0)
              g = (g / g.max()) * (255.0)
              r = (r / r.max()) * (255.0)

            cv2.imwrite(self.fname, cv2.merge((np.rint(b).astype(np.uint8),
                                               np.rint(g).astype(np.uint8),
                                               np.rint(r).astype(np.uint8))))

    # test the class
    test = Mandelbrot()
