#!/usr/bin/python
# Code to easily extract deep features from pre-trained networks using Caffe
# Author: Keiller Nogueira
# Date: June 28, 2018

import os
import shutil
import sys

import caffe
import numpy as np
import plyvel  # use 0.9
from caffe.proto import caffe_pb2


def create_AlexNet_prototxt(output_file, caffe_path, tmp_path):
    f = open(output_file, 'w')

    f.write("name: \"AlexNet\" \n\
    layer \n\
    { \n\
        name: \"data\" \n\
        type: \"ImageData\" \n\
        top: \"data\" \n\
        top: \"label\" \n\
        transform_param { \n\
            mirror: false \n\
            crop_size: 227 \n\
            mean_file: \"" + caffe_path + "/data/ilsvrc12/imagenet_mean.binaryproto\" \n\
        } \n\
        image_data_param { \n\
            source: \"" + str(os.path.join(tmp_path, 'file_list.txt')) + "\" \n\
            batch_size: 1 \n\
            new_height: 256 \n\
            new_width: 256 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"conv1\" \n\
        type: \"Convolution\" \n\
        bottom: \"data\" \n\
        top: \"conv1\" \n\
        convolution_param { \n\
            num_output: 96 \n\
            kernel_size: 11 \n\
            stride: 4 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"relu1\" \n\
        type: \"ReLU\" \n\
        bottom: \"conv1\" \n\
        top: \"conv1\" \n\
    } \n\
    layer \n\
    { \n\
        name: \"norm1\" \n\
        type: \"LRN\" \n\
        bottom: \"conv1\" \n\
        top: \"norm1\" \n\
        lrn_param { \n\
            local_size: 5 \n\
            alpha: 0.0001 \n\
            beta: 0.75 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"pool1\" \n\
        type: \"Pooling\" \n\
        bottom: \"norm1\" \n\
        top: \"pool1\" \n\
        pooling_param { \n\
            pool: MAX \n\
            kernel_size: 3 \n\
            stride: 2 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"conv2\" \n\
        type: \"Convolution\" \n\
        bottom: \"pool1\" \n\
        top: \"conv2\" \n\
        convolution_param { \n\
            num_output: 256 \n\
            pad: 2 \n\
            kernel_size: 5 \n\
            group: 2 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"relu2\" \n\
        type: \"ReLU\" \n\
        bottom: \"conv2\" \n\
        top: \"conv2\" \n\
    } \n\
    layer \n\
    { \n\
        name: \"norm2\" \n\
        type: \"LRN\" \n\
        bottom: \"conv2\" \n\
        top: \"norm2\" \n\
        lrn_param { \n\
            local_size: 5 \n\
            alpha: 0.0001 \n\
            beta: 0.75 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"pool2\" \n\
        type: \"Pooling\" \n\
        bottom: \"norm2\" \n\
        top: \"pool2\" \n\
        pooling_param { \n\
            pool: MAX \n\
            kernel_size: 3 \n\
            stride: 2 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"conv3\" \n\
        type: \"Convolution\" \n\
        bottom: \"pool2\" \n\
        top: \"conv3\" \n\
        convolution_param { \n\
            num_output: 384 \n\
            pad: 1 \n\
            kernel_size: 3 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"relu3\" \n\
        type: \"ReLU\" \n\
        bottom: \"conv3\" \n\
        top: \"conv3\" \n\
    } \n\
    layer \n\
    { \n\
        name: \"conv4\" \n\
        type: \"Convolution\" \n\
        bottom: \"conv3\" \n\
        top: \"conv4\" \n\
        convolution_param { \n\
            num_output: 384 \n\
            pad: 1 \n\
            kernel_size: 3 \n\
            group: 2 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"relu4\" \n\
        type: \"ReLU\" \n\
        bottom: \"conv4\" \n\
        top: \"conv4\" \n\
    } \n\
    layer \n\
    { \n\
        name: \"conv5\" \n\
        type: \"Convolution\" \n\
        bottom: \"conv4\" \n\
        top: \"conv5\" \n\
        convolution_param { \n\
            num_output: 256 \n\
            pad: 1 \n\
            kernel_size: 3 \n\
            group: 2 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"relu5\" \n\
        type: \"ReLU\" \n\
        bottom: \"conv5\" \n\
        top: \"conv5\" \n\
    } \n\
    layer \n\
    { \n\
        name: \"pool5\" \n\
        type: \"Pooling\" \n\
        bottom: \"conv5\" \n\
        top: \"pool5\" \n\
        pooling_param { \n\
            pool: MAX \n\
            kernel_size: 3 \n\
            stride: 2 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"fc6\" \n\
        type: \"InnerProduct\" \n\
        bottom: \"pool5\" \n\
        top: \"fc6\" \n\
        inner_product_param { \n\
            num_output: 4096 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"relu6\" \n\
        type: \"ReLU\" \n\
        bottom: \"fc6\" \n\
        top: \"fc6\" \n\
    } \n\
    layer \n\
    { \n\
        name: \"drop6\" \n\
        type: \"Dropout\" \n\
        bottom: \"fc6\" \n\
        top: \"fc6\" \n\
        dropout_param { \n\
            dropout_ratio: 0.5 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"fc7\" \n\
        type: \"InnerProduct\" \n\
        bottom: \"fc6\" \n\
        top: \"fc7\" \n\
        inner_product_param { \n\
            num_output: 4096 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"relu7\" \n\
        type: \"ReLU\" \n\
        bottom: \"fc7\" \n\
        top: \"fc7\" \n\
    } \n\
    layer \n\
    { \n\
        name: \"drop7\" \n\
        type: \"Dropout\" \n\
        bottom: \"fc7\" \n\
        top: \"fc7\" \n\
        dropout_param { \n\
            dropout_ratio: 0.5 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"fc8\" \n\
        type: \"InnerProduct\" \n\
        bottom: \"fc7\" \n\
        top: \"fc8\" \n\
        inner_product_param { \n\
            num_output: 1000 \n\
        } \n\
    } \n\
    layer \n\
    { \n\
        name: \"prob\" \n\
        type: \"Softmax\" \n\
        bottom: \"fc8\" \n\
        top: \"prob\" \n\
    } \n\
    layer \n\
    { \n\
        name: \"accuracy\" \n\
        type: \"Accuracy\" \n\
        bottom: \"prob\" \n\
        bottom: \"label\" \n\
        top: \"accuracy\" \n\
    } \n\
    layer \n\
    { \n\
        name: \"loss\" \n\
        type: \"SoftmaxWithLoss\" \n\
        bottom: \"fc8\" \n\
        bottom: \"label\" \n\
        top: \"loss\" \n\
    } \n ")

    f.close()


def create_CaffeNet_prototxt(output_file, caffe_path, tmp_path):
    f = open(output_file, 'w')

    f.write("name: \"CaffeNet\" \n\
    layer { \n\
      name: \"data\" \n\
      type: \"ImageData\" \n\
      top: \"data\" \n\
      top: \"label\" \n\
      transform_param { \n\
        mirror: false \n\
        crop_size: 227 \n\
        mean_file: \"" + caffe_path + "/data/ilsvrc12/imagenet_mean.binaryproto\" \n\
        } \n\
        image_data_param { \n\
        source: \"" + str(os.path.join(tmp_path, 'file_list.txt')) + "\" \n\
        batch_size: 1 \n\
        new_height: 256 \n\
        new_width: 256 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"conv1\" \n\
      type: \"Convolution\" \n\
      bottom: \"data\" \n\
      top: \"conv1\" \n\
      convolution_param { \n\
        num_output: 96 \n\
        kernel_size: 11 \n\
        stride: 4 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"relu1\" \n\
      type: \"ReLU\" \n\
      bottom: \"conv1\" \n\
      top: \"conv1\" \n\
    } \n\
    layer { \n\
      name: \"pool1\" \n\
      type: \"Pooling\" \n\
      bottom: \"conv1\" \n\
      top: \"pool1\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"norm1\" \n\
      type: \"LRN\" \n\
      bottom: \"pool1\" \n\
      top: \"norm1\" \n\
      lrn_param { \n\
        local_size: 5 \n\
        alpha: 0.0001 \n\
        beta: 0.75 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"conv2\" \n\
      type: \"Convolution\" \n\
      bottom: \"norm1\" \n\
      top: \"conv2\" \n\
      convolution_param { \n\
        num_output: 256 \n\
        pad: 2 \n\
        kernel_size: 5 \n\
        group: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"relu2\" \n\
      type: \"ReLU\" \n\
      bottom: \"conv2\" \n\
      top: \"conv2\" \n\
    } \n\
    layer { \n\
      name: \"pool2\" \n\
      type: \"Pooling\" \n\
      bottom: \"conv2\" \n\
      top: \"pool2\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"norm2\" \n\
      type: \"LRN\" \n\
      bottom: \"pool2\" \n\
      top: \"norm2\" \n\
      lrn_param { \n\
        local_size: 5 \n\
        alpha: 0.0001 \n\
        beta: 0.75 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"conv3\" \n\
      type: \"Convolution\" \n\
      bottom: \"norm2\" \n\
      top: \"conv3\" \n\
      convolution_param { \n\
        num_output: 384 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"relu3\" \n\
      type: \"ReLU\" \n\
      bottom: \"conv3\" \n\
      top: \"conv3\" \n\
    } \n\
    layer { \n\
      name: \"conv4\" \n\
      type: \"Convolution\" \n\
      bottom: \"conv3\" \n\
      top: \"conv4\" \n\
      convolution_param { \n\
        num_output: 384 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
        group: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"relu4\" \n\
      type: \"ReLU\" \n\
      bottom: \"conv4\" \n\
      top: \"conv4\" \n\
    } \n\
    layer { \n\
      name: \"conv5\" \n\
      type: \"Convolution\" \n\
      bottom: \"conv4\" \n\
      top: \"conv5\" \n\
      convolution_param { \n\
        num_output: 256 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
        group: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"relu5\" \n\
      type: \"ReLU\" \n\
      bottom: \"conv5\" \n\
      top: \"conv5\" \n\
    } \n\
    layer { \n\
      name: \"pool5\" \n\
      type: \"Pooling\" \n\
      bottom: \"conv5\" \n\
      top: \"pool5\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"fc6\" \n\
      type: \"InnerProduct\" \n\
      bottom: \"pool5\" \n\
      top: \"fc6\" \n\
      inner_product_param { \n\
        num_output: 4096 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"relu6\" \n\
      type: \"ReLU\" \n\
      bottom: \"fc6\" \n\
      top: \"fc6\" \n\
    } \n\
    layer { \n\
      name: \"drop6\" \n\
      type: \"Dropout\" \n\
      bottom: \"fc6\" \n\
      top: \"fc6\" \n\
      dropout_param { \n\
        dropout_ratio: 0.5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"fc7\" \n\
      type: \"InnerProduct\" \n\
      bottom: \"fc6\" \n\
      top: \"fc7\" \n\
      inner_product_param { \n\
        num_output: 4096 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"relu7\" \n\
      type: \"ReLU\" \n\
      bottom: \"fc7\" \n\
      top: \"fc7\" \n\
    } \n\
    layer { \n\
      name: \"drop7\" \n\
      type: \"Dropout\" \n\
      bottom: \"fc7\" \n\
      top: \"fc7\" \n\
      dropout_param { \n\
        dropout_ratio: 0.5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"fc8\" \n\
      type: \"InnerProduct\" \n\
      bottom: \"fc7\" \n\
      top: \"fc8\" \n\
      inner_product_param { \n\
        num_output: 1000 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"prob\" \n\
      type: \"Softmax\" \n\
      bottom: \"fc8\" \n\
      top: \"prob\" \n\
    } \n\
    layer { \n\
      name: \"accuracy\" \n\
      type: \"Accuracy\" \n\
      bottom: \"prob\" \n\
      bottom: \"label\" \n\
      top: \"accuracy\" \n\
    } \n\
    layer { \n\
      name: \"loss\" \n\
      type: \"SoftmaxWithLoss\" \n\
      bottom: \"fc8\" \n\
      bottom: \"label\" \n\
      top: \"loss\" \n\
    } \n ")

    f.close()


def create_GoogLeNet_prototxt(output_file, caffe_path, tmp_path):
    f = open(output_file, 'w')

    f.write("name: \"GoogleNet\" \n\
    layer { \n\
      name: \"data\" \n\
      type: \"ImageData\" \n\
      top: \"data\" \n\
      top: \"label\" \n\
      transform_param { \n\
        mirror: false \n\
        crop_size: 224 \n\
        mean_file: \"" + caffe_path + "/data/ilsvrc12/imagenet_mean.binaryproto\" \n\
      } \n\
      image_data_param { \n\
        source: \"" + str(os.path.join(tmp_path, 'file_list.txt')) + "\" \n\
        batch_size: 1 \n\
        new_height: 256 \n\
        new_width: 256 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"conv1/7x7_s2\" \n\
      type: \"Convolution\" \n\
      bottom: \"data\" \n\
      top: \"conv1/7x7_s2\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        pad: 3 \n\
        kernel_size: 7 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"conv1/relu_7x7\" \n\
      type: \"ReLU\" \n\
      bottom: \"conv1/7x7_s2\" \n\
      top: \"conv1/7x7_s2\" \n\
    } \n\
    layer { \n\
      name: \"pool1/3x3_s2\" \n\
      type: \"Pooling\" \n\
      bottom: \"conv1/7x7_s2\" \n\
      top: \"pool1/3x3_s2\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"pool1/norm1\" \n\
      type: \"LRN\" \n\
      bottom: \"pool1/3x3_s2\" \n\
      top: \"pool1/norm1\" \n\
      lrn_param { \n\
        local_size: 5 \n\
        alpha: 0.0001 \n\
        beta: 0.75 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"conv2/3x3_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"pool1/norm1\" \n\
      top: \"conv2/3x3_reduce\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"conv2/relu_3x3_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"conv2/3x3_reduce\" \n\
      top: \"conv2/3x3_reduce\" \n\
    } \n\
    layer { \n\
      name: \"conv2/3x3\" \n\
      type: \"Convolution\" \n\
      bottom: \"conv2/3x3_reduce\" \n\
      top: \"conv2/3x3\" \n\
      convolution_param { \n\
        num_output: 192 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"conv2/relu_3x3\" \n\
      type: \"ReLU\" \n\
      bottom: \"conv2/3x3\" \n\
      top: \"conv2/3x3\" \n\
    } \n\
    layer { \n\
      name: \"conv2/norm2\" \n\
      type: \"LRN\" \n\
      bottom: \"conv2/3x3\" \n\
      top: \"conv2/norm2\" \n\
      lrn_param { \n\
        local_size: 5 \n\
        alpha: 0.0001 \n\
        beta: 0.75 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"pool2/3x3_s2\" \n\
      type: \"Pooling\" \n\
      bottom: \"conv2/norm2\" \n\
      top: \"pool2/3x3_s2\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3a/1x1\" \n\
      type: \"Convolution\" \n\
      bottom: \"pool2/3x3_s2\" \n\
      top: \"inception_3a/1x1\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3a/relu_1x1\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3a/1x1\" \n\
      top: \"inception_3a/1x1\" \n\
    } \n\
    layer { \n\
      name: \"inception_3a/3x3_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"pool2/3x3_s2\" \n\
      top: \"inception_3a/3x3_reduce\" \n\
      convolution_param { \n\
        num_output: 96 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3a/relu_3x3_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3a/3x3_reduce\" \n\
      top: \"inception_3a/3x3_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_3a/3x3\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_3a/3x3_reduce\" \n\
      top: \"inception_3a/3x3\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3a/relu_3x3\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3a/3x3\" \n\
      top: \"inception_3a/3x3\" \n\
    } \n\
    layer { \n\
      name: \"inception_3a/5x5_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"pool2/3x3_s2\" \n\
      top: \"inception_3a/5x5_reduce\" \n\
      convolution_param { \n\
        num_output: 16 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3a/relu_5x5_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3a/5x5_reduce\" \n\
      top: \"inception_3a/5x5_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_3a/5x5\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_3a/5x5_reduce\" \n\
      top: \"inception_3a/5x5\" \n\
      convolution_param { \n\
        num_output: 32 \n\
        pad: 2 \n\
        kernel_size: 5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3a/relu_5x5\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3a/5x5\" \n\
      top: \"inception_3a/5x5\" \n\
    } \n\
    layer { \n\
      name: \"inception_3a/pool\" \n\
      type: \"Pooling\" \n\
      bottom: \"pool2/3x3_s2\" \n\
      top: \"inception_3a/pool\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 1 \n\
        pad: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3a/pool_proj\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_3a/pool\" \n\
      top: \"inception_3a/pool_proj\" \n\
      convolution_param { \n\
        num_output: 32 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3a/relu_pool_proj\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3a/pool_proj\" \n\
      top: \"inception_3a/pool_proj\" \n\
    } \n\
    layer { \n\
      name: \"inception_3a/output\" \n\
      type: \"Concat\" \n\
      bottom: \"inception_3a/1x1\" \n\
      bottom: \"inception_3a/3x3\" \n\
      bottom: \"inception_3a/5x5\" \n\
      bottom: \"inception_3a/pool_proj\" \n\
      top: \"inception_3a/output\" \n\
    } \n\
    layer { \n\
      name: \"inception_3b/1x1\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_3a/output\" \n\
      top: \"inception_3b/1x1\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3b/relu_1x1\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3b/1x1\" \n\
      top: \"inception_3b/1x1\" \n\
    } \n\
    layer { \n\
      name: \"inception_3b/3x3_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_3a/output\" \n\
      top: \"inception_3b/3x3_reduce\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3b/relu_3x3_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3b/3x3_reduce\" \n\
      top: \"inception_3b/3x3_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_3b/3x3\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_3b/3x3_reduce\" \n\
      top: \"inception_3b/3x3\" \n\
      convolution_param { \n\
        num_output: 192 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3b/relu_3x3\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3b/3x3\" \n\
      top: \"inception_3b/3x3\" \n\
    } \n\
    layer { \n\
      name: \"inception_3b/5x5_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_3a/output\" \n\
      top: \"inception_3b/5x5_reduce\" \n\
      convolution_param { \n\
        num_output: 32 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3b/relu_5x5_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3b/5x5_reduce\" \n\
      top: \"inception_3b/5x5_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_3b/5x5\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_3b/5x5_reduce\" \n\
      top: \"inception_3b/5x5\" \n\
      convolution_param { \n\
        num_output: 96 \n\
        pad: 2 \n\
        kernel_size: 5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3b/relu_5x5\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3b/5x5\" \n\
      top: \"inception_3b/5x5\" \n\
    } \n\
    layer { \n\
      name: \"inception_3b/pool\" \n\
      type: \"Pooling\" \n\
      bottom: \"inception_3a/output\" \n\
      top: \"inception_3b/pool\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 1 \n\
        pad: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3b/pool_proj\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_3b/pool\" \n\
      top: \"inception_3b/pool_proj\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_3b/relu_pool_proj\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_3b/pool_proj\" \n\
      top: \"inception_3b/pool_proj\" \n\
    } \n\
    layer { \n\
      name: \"inception_3b/output\" \n\
      type: \"Concat\" \n\
      bottom: \"inception_3b/1x1\" \n\
      bottom: \"inception_3b/3x3\" \n\
      bottom: \"inception_3b/5x5\" \n\
      bottom: \"inception_3b/pool_proj\" \n\
      top: \"inception_3b/output\" \n\
    } \n\
    layer { \n\
      name: \"pool3/3x3_s2\" \n\
      type: \"Pooling\" \n\
      bottom: \"inception_3b/output\" \n\
      top: \"pool3/3x3_s2\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4a/1x1\" \n\
      type: \"Convolution\" \n\
      bottom: \"pool3/3x3_s2\" \n\
      top: \"inception_4a/1x1\" \n\
      convolution_param { \n\
        num_output: 192 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4a/relu_1x1\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4a/1x1\" \n\
      top: \"inception_4a/1x1\" \n\
    } \n\
    layer { \n\
      name: \"inception_4a/3x3_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"pool3/3x3_s2\" \n\
      top: \"inception_4a/3x3_reduce\" \n\
      convolution_param { \n\
        num_output: 96 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4a/relu_3x3_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4a/3x3_reduce\" \n\
      top: \"inception_4a/3x3_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_4a/3x3\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4a/3x3_reduce\" \n\
      top: \"inception_4a/3x3\" \n\
      convolution_param { \n\
        num_output: 208 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4a/relu_3x3\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4a/3x3\" \n\
      top: \"inception_4a/3x3\" \n\
    } \n\
    layer { \n\
      name: \"inception_4a/5x5_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"pool3/3x3_s2\" \n\
      top: \"inception_4a/5x5_reduce\" \n\
      convolution_param { \n\
        num_output: 16 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4a/relu_5x5_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4a/5x5_reduce\" \n\
      top: \"inception_4a/5x5_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_4a/5x5\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4a/5x5_reduce\" \n\
      top: \"inception_4a/5x5\" \n\
      convolution_param { \n\
        num_output: 48 \n\
        pad: 2 \n\
        kernel_size: 5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4a/relu_5x5\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4a/5x5\" \n\
      top: \"inception_4a/5x5\" \n\
    } \n\
    layer { \n\
      name: \"inception_4a/pool\" \n\
      type: \"Pooling\" \n\
      bottom: \"pool3/3x3_s2\" \n\
      top: \"inception_4a/pool\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 1 \n\
        pad: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4a/pool_proj\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4a/pool\" \n\
      top: \"inception_4a/pool_proj\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4a/relu_pool_proj\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4a/pool_proj\" \n\
      top: \"inception_4a/pool_proj\" \n\
    } \n\
    layer { \n\
      name: \"inception_4a/output\" \n\
      type: \"Concat\" \n\
      bottom: \"inception_4a/1x1\" \n\
      bottom: \"inception_4a/3x3\" \n\
      bottom: \"inception_4a/5x5\" \n\
      bottom: \"inception_4a/pool_proj\" \n\
      top: \"inception_4a/output\" \n\
    } \n\
    layer { \n\
      name: \"inception_4b/1x1\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4a/output\" \n\
      top: \"inception_4b/1x1\" \n\
      convolution_param { \n\
        num_output: 160 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4b/relu_1x1\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4b/1x1\" \n\
      top: \"inception_4b/1x1\" \n\
    } \n\
    layer { \n\
      name: \"inception_4b/3x3_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4a/output\" \n\
      top: \"inception_4b/3x3_reduce\" \n\
      convolution_param { \n\
        num_output: 112 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4b/relu_3x3_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4b/3x3_reduce\" \n\
      top: \"inception_4b/3x3_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_4b/3x3\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4b/3x3_reduce\" \n\
      top: \"inception_4b/3x3\" \n\
      convolution_param { \n\
        num_output: 224 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4b/relu_3x3\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4b/3x3\" \n\
      top: \"inception_4b/3x3\" \n\
    } \n\
    layer { \n\
      name: \"inception_4b/5x5_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4a/output\" \n\
      top: \"inception_4b/5x5_reduce\" \n\
      convolution_param { \n\
        num_output: 24 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4b/relu_5x5_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4b/5x5_reduce\" \n\
      top: \"inception_4b/5x5_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_4b/5x5\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4b/5x5_reduce\" \n\
      top: \"inception_4b/5x5\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        pad: 2 \n\
        kernel_size: 5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4b/relu_5x5\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4b/5x5\" \n\
      top: \"inception_4b/5x5\" \n\
    } \n\
    layer { \n\
      name: \"inception_4b/pool\" \n\
      type: \"Pooling\" \n\
      bottom: \"inception_4a/output\" \n\
      top: \"inception_4b/pool\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 1 \n\
        pad: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4b/pool_proj\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4b/pool\" \n\
      top: \"inception_4b/pool_proj\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4b/relu_pool_proj\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4b/pool_proj\" \n\
      top: \"inception_4b/pool_proj\" \n\
    } \n\
    layer { \n\
      name: \"inception_4b/output\" \n\
      type: \"Concat\" \n\
      bottom: \"inception_4b/1x1\" \n\
      bottom: \"inception_4b/3x3\" \n\
      bottom: \"inception_4b/5x5\" \n\
      bottom: \"inception_4b/pool_proj\" \n\
      top: \"inception_4b/output\" \n\
    } \n\
    layer { \n\
      name: \"inception_4c/1x1\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4b/output\" \n\
      top: \"inception_4c/1x1\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4c/relu_1x1\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4c/1x1\" \n\
      top: \"inception_4c/1x1\" \n\
    } \n\
    layer { \n\
      name: \"inception_4c/3x3_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4b/output\" \n\
      top: \"inception_4c/3x3_reduce\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4c/relu_3x3_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4c/3x3_reduce\" \n\
      top: \"inception_4c/3x3_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_4c/3x3\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4c/3x3_reduce\" \n\
      top: \"inception_4c/3x3\" \n\
      convolution_param { \n\
        num_output: 256 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4c/relu_3x3\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4c/3x3\" \n\
      top: \"inception_4c/3x3\" \n\
    } \n\
    layer { \n\
      name: \"inception_4c/5x5_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4b/output\" \n\
      top: \"inception_4c/5x5_reduce\" \n\
      convolution_param { \n\
        num_output: 24 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4c/relu_5x5_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4c/5x5_reduce\" \n\
      top: \"inception_4c/5x5_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_4c/5x5\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4c/5x5_reduce\" \n\
      top: \"inception_4c/5x5\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        pad: 2 \n\
        kernel_size: 5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4c/relu_5x5\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4c/5x5\" \n\
      top: \"inception_4c/5x5\" \n\
    } \n\
    layer { \n\
      name: \"inception_4c/pool\" \n\
      type: \"Pooling\" \n\
      bottom: \"inception_4b/output\" \n\
      top: \"inception_4c/pool\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 1 \n\
        pad: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4c/pool_proj\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4c/pool\" \n\
      top: \"inception_4c/pool_proj\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4c/relu_pool_proj\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4c/pool_proj\" \n\
      top: \"inception_4c/pool_proj\" \n\
    } \n\
    layer { \n\
      name: \"inception_4c/output\" \n\
      type: \"Concat\" \n\
      bottom: \"inception_4c/1x1\" \n\
      bottom: \"inception_4c/3x3\" \n\
      bottom: \"inception_4c/5x5\" \n\
      bottom: \"inception_4c/pool_proj\" \n\
      top: \"inception_4c/output\" \n\
    } \n\
    layer { \n\
      name: \"inception_4d/1x1\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4c/output\" \n\
      top: \"inception_4d/1x1\" \n\
      convolution_param { \n\
        num_output: 112 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4d/relu_1x1\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4d/1x1\" \n\
      top: \"inception_4d/1x1\" \n\
    } \n\
    layer { \n\
      name: \"inception_4d/3x3_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4c/output\" \n\
      top: \"inception_4d/3x3_reduce\" \n\
      convolution_param { \n\
        num_output: 144 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4d/relu_3x3_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4d/3x3_reduce\" \n\
      top: \"inception_4d/3x3_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_4d/3x3\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4d/3x3_reduce\" \n\
      top: \"inception_4d/3x3\" \n\
      convolution_param { \n\
        num_output: 288 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4d/relu_3x3\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4d/3x3\" \n\
      top: \"inception_4d/3x3\" \n\
    } \n\
    layer { \n\
      name: \"inception_4d/5x5_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4c/output\" \n\
      top: \"inception_4d/5x5_reduce\" \n\
      convolution_param { \n\
        num_output: 32 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4d/relu_5x5_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4d/5x5_reduce\" \n\
      top: \"inception_4d/5x5_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_4d/5x5\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4d/5x5_reduce\" \n\
      top: \"inception_4d/5x5\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        pad: 2 \n\
        kernel_size: 5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4d/relu_5x5\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4d/5x5\" \n\
      top: \"inception_4d/5x5\" \n\
    } \n\
    layer { \n\
      name: \"inception_4d/pool\" \n\
      type: \"Pooling\" \n\
      bottom: \"inception_4c/output\" \n\
      top: \"inception_4d/pool\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 1 \n\
        pad: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4d/pool_proj\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4d/pool\" \n\
      top: \"inception_4d/pool_proj\" \n\
      convolution_param { \n\
        num_output: 64 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4d/relu_pool_proj\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4d/pool_proj\" \n\
      top: \"inception_4d/pool_proj\" \n\
    } \n\
    layer { \n\
      name: \"inception_4d/output\" \n\
      type: \"Concat\" \n\
      bottom: \"inception_4d/1x1\" \n\
      bottom: \"inception_4d/3x3\" \n\
      bottom: \"inception_4d/5x5\" \n\
      bottom: \"inception_4d/pool_proj\" \n\
      top: \"inception_4d/output\" \n\
    } \n\
    layer { \n\
      name: \"inception_4e/1x1\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4d/output\" \n\
      top: \"inception_4e/1x1\" \n\
      convolution_param { \n\
        num_output: 256 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4e/relu_1x1\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4e/1x1\" \n\
      top: \"inception_4e/1x1\" \n\
    } \n\
    layer { \n\
      name: \"inception_4e/3x3_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4d/output\" \n\
      top: \"inception_4e/3x3_reduce\" \n\
      convolution_param { \n\
        num_output: 160 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4e/relu_3x3_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4e/3x3_reduce\" \n\
      top: \"inception_4e/3x3_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_4e/3x3\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4e/3x3_reduce\" \n\
      top: \"inception_4e/3x3\" \n\
      convolution_param { \n\
        num_output: 320 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4e/relu_3x3\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4e/3x3\" \n\
      top: \"inception_4e/3x3\" \n\
    } \n\
    layer { \n\
      name: \"inception_4e/5x5_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4d/output\" \n\
      top: \"inception_4e/5x5_reduce\" \n\
      convolution_param { \n\
        num_output: 32 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4e/relu_5x5_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4e/5x5_reduce\" \n\
      top: \"inception_4e/5x5_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_4e/5x5\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4e/5x5_reduce\" \n\
      top: \"inception_4e/5x5\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        pad: 2 \n\
        kernel_size: 5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4e/relu_5x5\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4e/5x5\" \n\
      top: \"inception_4e/5x5\" \n\
    } \n\
    layer { \n\
      name: \"inception_4e/pool\" \n\
      type: \"Pooling\" \n\
      bottom: \"inception_4d/output\" \n\
      top: \"inception_4e/pool\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 1 \n\
        pad: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4e/pool_proj\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_4e/pool\" \n\
      top: \"inception_4e/pool_proj\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_4e/relu_pool_proj\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_4e/pool_proj\" \n\
      top: \"inception_4e/pool_proj\" \n\
    } \n\
    layer { \n\
      name: \"inception_4e/output\" \n\
      type: \"Concat\" \n\
      bottom: \"inception_4e/1x1\" \n\
      bottom: \"inception_4e/3x3\" \n\
      bottom: \"inception_4e/5x5\" \n\
      bottom: \"inception_4e/pool_proj\" \n\
      top: \"inception_4e/output\" \n\
    } \n\
    layer { \n\
      name: \"pool4/3x3_s2\" \n\
      type: \"Pooling\" \n\
      bottom: \"inception_4e/output\" \n\
      top: \"pool4/3x3_s2\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5a/1x1\" \n\
      type: \"Convolution\" \n\
      bottom: \"pool4/3x3_s2\" \n\
      top: \"inception_5a/1x1\" \n\
      convolution_param { \n\
        num_output: 256 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5a/relu_1x1\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5a/1x1\" \n\
      top: \"inception_5a/1x1\" \n\
    } \n\
    layer { \n\
      name: \"inception_5a/3x3_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"pool4/3x3_s2\" \n\
      top: \"inception_5a/3x3_reduce\" \n\
      convolution_param { \n\
        num_output: 160 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5a/relu_3x3_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5a/3x3_reduce\" \n\
      top: \"inception_5a/3x3_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_5a/3x3\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_5a/3x3_reduce\" \n\
      top: \"inception_5a/3x3\" \n\
      convolution_param { \n\
        num_output: 320 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5a/relu_3x3\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5a/3x3\" \n\
      top: \"inception_5a/3x3\" \n\
    } \n\
    layer { \n\
      name: \"inception_5a/5x5_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"pool4/3x3_s2\" \n\
      top: \"inception_5a/5x5_reduce\" \n\
      convolution_param { \n\
        num_output: 32 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5a/relu_5x5_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5a/5x5_reduce\" \n\
      top: \"inception_5a/5x5_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_5a/5x5\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_5a/5x5_reduce\" \n\
      top: \"inception_5a/5x5\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        pad: 2 \n\
        kernel_size: 5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5a/relu_5x5\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5a/5x5\" \n\
      top: \"inception_5a/5x5\" \n\
    } \n\
    layer { \n\
      name: \"inception_5a/pool\" \n\
      type: \"Pooling\" \n\
      bottom: \"pool4/3x3_s2\" \n\
      top: \"inception_5a/pool\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 1 \n\
        pad: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5a/pool_proj\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_5a/pool\" \n\
      top: \"inception_5a/pool_proj\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5a/relu_pool_proj\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5a/pool_proj\" \n\
      top: \"inception_5a/pool_proj\" \n\
    } \n\
    layer { \n\
      name: \"inception_5a/output\" \n\
      type: \"Concat\" \n\
      bottom: \"inception_5a/1x1\" \n\
      bottom: \"inception_5a/3x3\" \n\
      bottom: \"inception_5a/5x5\" \n\
      bottom: \"inception_5a/pool_proj\" \n\
      top: \"inception_5a/output\" \n\
    } \n\
    layer { \n\
      name: \"inception_5b/1x1\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_5a/output\" \n\
      top: \"inception_5b/1x1\" \n\
      convolution_param { \n\
        num_output: 384 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5b/relu_1x1\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5b/1x1\" \n\
      top: \"inception_5b/1x1\" \n\
    } \n\
    layer { \n\
      name: \"inception_5b/3x3_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_5a/output\" \n\
      top: \"inception_5b/3x3_reduce\" \n\
      convolution_param { \n\
        num_output: 192 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5b/relu_3x3_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5b/3x3_reduce\" \n\
      top: \"inception_5b/3x3_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_5b/3x3\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_5b/3x3_reduce\" \n\
      top: \"inception_5b/3x3\" \n\
      convolution_param { \n\
        num_output: 384 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5b/relu_3x3\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5b/3x3\" \n\
      top: \"inception_5b/3x3\" \n\
    } \n\
    layer { \n\
      name: \"inception_5b/5x5_reduce\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_5a/output\" \n\
      top: \"inception_5b/5x5_reduce\" \n\
      convolution_param { \n\
        num_output: 48 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5b/relu_5x5_reduce\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5b/5x5_reduce\" \n\
      top: \"inception_5b/5x5_reduce\" \n\
    } \n\
    layer { \n\
      name: \"inception_5b/5x5\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_5b/5x5_reduce\" \n\
      top: \"inception_5b/5x5\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        pad: 2 \n\
        kernel_size: 5 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5b/relu_5x5\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5b/5x5\" \n\
      top: \"inception_5b/5x5\" \n\
    } \n\
    layer { \n\
      name: \"inception_5b/pool\" \n\
      type: \"Pooling\" \n\
      bottom: \"inception_5a/output\" \n\
      top: \"inception_5b/pool\" \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 3 \n\
        stride: 1 \n\
        pad: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5b/pool_proj\" \n\
      type: \"Convolution\" \n\
      bottom: \"inception_5b/pool\" \n\
      top: \"inception_5b/pool_proj\" \n\
      convolution_param { \n\
        num_output: 128 \n\
        kernel_size: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"inception_5b/relu_pool_proj\" \n\
      type: \"ReLU\" \n\
      bottom: \"inception_5b/pool_proj\" \n\
      top: \"inception_5b/pool_proj\" \n\
    } \n\
    layer { \n\
      name: \"inception_5b/output\" \n\
      type: \"Concat\" \n\
      bottom: \"inception_5b/1x1\" \n\
      bottom: \"inception_5b/3x3\" \n\
      bottom: \"inception_5b/5x5\" \n\
      bottom: \"inception_5b/pool_proj\" \n\
      top: \"inception_5b/output\" \n\
    } \n\
    layer { \n\
      name: \"pool5/7x7_s1\" \n\
      type: \"Pooling\" \n\
      bottom: \"inception_5b/output\" \n\
      top: \"pool5/7x7_s1\" \n\
      pooling_param { \n\
        pool: AVE \n\
        kernel_size: 7 \n\
        stride: 1 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"pool5/drop_7x7_s1\" \n\
      type: \"Dropout\" \n\
      bottom: \"pool5/7x7_s1\" \n\
      top: \"pool5/7x7_s1\" \n\
      dropout_param { \n\
        dropout_ratio: 0.4 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"loss3/classifier\" \n\
      type: \"InnerProduct\" \n\
      bottom: \"pool5/7x7_s1\" \n\
      top: \"loss3/classifier\" \n\
      inner_product_param { \n\
        num_output: 1000 \n\
      } \n\
    } \n\
    layer { \n\
      name: \"prob\" \n\
      type: \"Softmax\" \n\
      bottom: \"loss3/classifier\" \n\
      top: \"prob\" \n\
    } \n ")

    f.close()


def create_VGG16_prototxt(output_file, caffe_path, tmp_path):
    f = open(output_file, 'w')

    f.write("name: \"VGG_ILSVRC_16_layers\" \n\
    layers { \n\
      name: \"data\" \n\
      type: IMAGE_DATA \n\
      top: \"data\" \n\
      top: \"label\" \n\
      transform_param { \n\
        mirror: false \n\
        crop_size: 224 \n\
        mean_file: \"" + caffe_path + "/data/ilsvrc12/imagenet_mean.binaryproto\" \n\
        } \n\
        image_data_param { \n\
        source: \"" + str(os.path.join(tmp_path, 'file_list.txt')) + "\" \n\
        batch_size: 1 \n\
        new_height: 256 \n\
        new_width: 256 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"data\" \n\
      top: \"conv1_1\" \n\
      name: \"conv1_1\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 64 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv1_1\" \n\
      top: \"conv1_1\" \n\
      name: \"relu1_1\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv1_1\" \n\
      top: \"conv1_2\" \n\
      name: \"conv1_2\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 64 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv1_2\" \n\
      top: \"conv1_2\" \n\
      name: \"relu1_2\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv1_2\" \n\
      top: \"pool1\" \n\
      name: \"pool1\" \n\
      type: POOLING \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 2 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"pool1\" \n\
      top: \"conv2_1\" \n\
      name: \"conv2_1\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 128 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv2_1\" \n\
      top: \"conv2_1\" \n\
      name: \"relu2_1\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv2_1\" \n\
      top: \"conv2_2\" \n\
      name: \"conv2_2\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 128 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv2_2\" \n\
      top: \"conv2_2\" \n\
      name: \"relu2_2\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv2_2\" \n\
      top: \"pool2\" \n\
      name: \"pool2\" \n\
      type: POOLING \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 2 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"pool2\" \n\
      top: \"conv3_1\" \n\
      name: \"conv3_1\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 256 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv3_1\" \n\
      top: \"conv3_1\" \n\
      name: \"relu3_1\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv3_1\" \n\
      top: \"conv3_2\" \n\
      name: \"conv3_2\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 256 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv3_2\" \n\
      top: \"conv3_2\" \n\
      name: \"relu3_2\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv3_2\" \n\
      top: \"conv3_3\" \n\
      name: \"conv3_3\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 256 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv3_3\" \n\
      top: \"conv3_3\" \n\
      name: \"relu3_3\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv3_3\" \n\
      top: \"pool3\" \n\
      name: \"pool3\" \n\
      type: POOLING \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 2 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"pool3\" \n\
      top: \"conv4_1\" \n\
      name: \"conv4_1\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 512 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv4_1\" \n\
      top: \"conv4_1\" \n\
      name: \"relu4_1\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv4_1\" \n\
      top: \"conv4_2\" \n\
      name: \"conv4_2\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 512 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv4_2\" \n\
      top: \"conv4_2\" \n\
      name: \"relu4_2\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv4_2\" \n\
      top: \"conv4_3\" \n\
      name: \"conv4_3\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 512 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv4_3\" \n\
      top: \"conv4_3\" \n\
      name: \"relu4_3\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv4_3\" \n\
      top: \"pool4\" \n\
      name: \"pool4\" \n\
      type: POOLING \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 2 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"pool4\" \n\
      top: \"conv5_1\" \n\
      name: \"conv5_1\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 512 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv5_1\" \n\
      top: \"conv5_1\" \n\
      name: \"relu5_1\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv5_1\" \n\
      top: \"conv5_2\" \n\
      name: \"conv5_2\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 512 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv5_2\" \n\
      top: \"conv5_2\" \n\
      name: \"relu5_2\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv5_2\" \n\
      top: \"conv5_3\" \n\
      name: \"conv5_3\" \n\
      type: CONVOLUTION \n\
      convolution_param { \n\
        num_output: 512 \n\
        pad: 1 \n\
        kernel_size: 3 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"conv5_3\" \n\
      top: \"conv5_3\" \n\
      name: \"relu5_3\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"conv5_3\" \n\
      top: \"pool5\" \n\
      name: \"pool5\" \n\
      type: POOLING \n\
      pooling_param { \n\
        pool: MAX \n\
        kernel_size: 2 \n\
        stride: 2 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"pool5\" \n\
      top: \"fc6\" \n\
      name: \"fc6\" \n\
      type: INNER_PRODUCT \n\
      inner_product_param { \n\
        num_output: 4096 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"fc6\" \n\
      top: \"fc6\" \n\
      name: \"relu6\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"fc6\" \n\
      top: \"fc6\" \n\
      name: \"drop6\" \n\
      type: DROPOUT \n\
      dropout_param { \n\
        dropout_ratio: 0.5 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"fc6\" \n\
      top: \"fc7\" \n\
      name: \"fc7\" \n\
      type: INNER_PRODUCT \n\
      inner_product_param { \n\
        num_output: 4096 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"fc7\" \n\
      top: \"fc7\" \n\
      name: \"relu7\" \n\
      type: RELU \n\
    } \n\
    layers { \n\
      bottom: \"fc7\" \n\
      top: \"fc7\" \n\
      name: \"drop7\" \n\
      type: DROPOUT \n\
      dropout_param { \n\
        dropout_ratio: 0.5 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"fc7\" \n\
      top: \"fc8\" \n\
      name: \"fc8\" \n\
      type: INNER_PRODUCT \n\
      inner_product_param { \n\
        num_output: 1000 \n\
      } \n\
    } \n\
    layers { \n\
      bottom: \"fc8\" \n\
      top: \"prob\" \n\
      name: \"prob\" \n\
      type: SOFTMAX \n\
    } \n ")

    f.close()


def print_params(list_params):
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    for i in xrange(1, len(sys.argv)):
        print(list_params[i - 1] + '= ' + sys.argv[i])
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')


def run_command(command, debug=False):
    if debug is True:
        print command
    os.system(command)


def get_imagenet_mean(caffe_path):
    run_command('sh ' + os.path.join(caffe_path, 'data/ilsvrc12/get_ilsvrc_aux.sh'))


def from_leveldb_to_txt(db_path, file_path, keys_path):
    db = plyvel.DB(db_path, create_if_missing=False)

    f = open(file_path, 'w')
    f_keys = open(keys_path, 'w')

    for key, value in db:
        datum = caffe_pb2.Datum.FromString(value)
        arr = caffe.io.datum_to_array(datum)
        tmp_list = arr.tolist()
        f.write(str(tmp_list) + "\n")
        f_keys.write(key + "\n")

    f_keys.close()
    f.close()
    db.close()


def create_final_files(leveldb, keys, files, output_file, num_images=None, num_features=None):
    try:
        f_leveldb = open(leveldb, 'r')
        f_keys = open(keys, 'r')
        f_files = open(files, 'r')
    except IOError:
        print "Could not open file!"
        print f_leveldb
        print f_keys
        print f_files
        return

    list_leveldb = []
    for line in f_leveldb:
        if line[-1] == "\n":
            line = line[:-1]
        list_leveldb.append(line)

    list_keys = []
    for line in f_keys:
        if line[-1] == "\n":
            line = line[:-1]
        list_keys.append(int(line.split(' ')[0]))

    list_files = []
    for line in f_files:
        if line[-1] == "\n":
            line = line[:-1]
        list_files.append(line[:-2].split('/')[-1].split('.')[0])

    # double check
    assert len(list_leveldb) == len(list_keys)
    assert len(list_leveldb) == len(list_files)
    ordered_leveldb = []
    for j in range(0, len(list_files)):
        index = list_keys.index(j)
        ordered_leveldb.append(list_leveldb[index])

    f_ordered = open(output_file, 'w')
    for j in range(0, len(ordered_leveldb)):
        new_level = ordered_leveldb[j].replace("[", "").replace("]", "")
        arr = np.fromstring(new_level, dtype=float, sep=",")

        f_ordered.write(list_files[j] + ",")
        for k in xrange(len(arr)):
            if k + 1 == len(arr):
                f_ordered.write(str(arr[k]) + "\n")
            else:
                f_ordered.write(str(arr[k]) + ",")

    f_leveldb.close()
    f_keys.close()
    f_files.close()
    f_ordered.close()


DICT_MODELS = {
    'AlexNet': ['http://dl.caffe.berkeleyvision.org/bvlc_alexnet.caffemodel',
                'fc7',
                create_AlexNet_prototxt],
    'CaffeNet': ['http://dl.caffe.berkeleyvision.org/bvlc_reference_caffenet.caffemodel',
                 'fc7',
                 create_CaffeNet_prototxt],
    'GoogLeNet': ['http://dl.caffe.berkeleyvision.org/bvlc_googlenet.caffemodel',
                  'pool5/7x7_s1',
                  create_GoogLeNet_prototxt],
    'VGG16': ['http://www.robots.ox.ac.uk/%7Evgg/software/very_deep/caffe/VGG_ILSVRC_16_layers.caffemodel',
              'fc7',
              create_VGG16_prototxt]}


def main():
    # python caffe_extract_features.py /opt/caffe/ /home/UCMerced/Images/ /home/UCMerced/Images/AlexNet/ AlexNet CPU
    list_params = ['caffe_path (MUST have execution permissions)', 'dataset_path',
                   'output_path', 'network [AlexNet | CaffeNet | GoogLeNet | VGG16]', 'CPU | GPU']
    if len(sys.argv) < len(list_params) + 1:
        sys.exit('Usage: ' + sys.argv[0] + ' ' + ' '.join(list_params))
    print_params(list_params)

    index = 1
    caffe_path = sys.argv[index]
    index = index + 1
    dataset_path = sys.argv[index]
    number_files = sum([len(files) for r, d, files in os.walk(dataset_path)])
    index = index + 1
    output_path = sys.argv[index]
    index = index + 1
    network = sys.argv[index]
    index = index + 1
    GPU_CPU = sys.argv[index]

    if network not in DICT_MODELS:
        print 'Network ' + network + ' not implemented yet.'
        print 'Options are: AlexNet, CaffeNet, GoogLeNet, and VGG16.'
        print 'Feel free to improve the code. ;)'
        return

    if not os.path.isfile(os.path.join(output_path, network + '_features.txt')):
        tmp_path = os.path.join(os.getcwd(), 'tmp/')
        if not os.path.exists(tmp_path):
            os.makedirs(tmp_path)

        # create file with all images to extract feature for
        run_command('find ' + dataset_path + ' -type f -exec echo {} \; > ' + os.path.join(tmp_path, 'temp.txt'))
        # add 0 to file for standard of caffe
        run_command('sed \"s/$/ 0/\" ' + os.path.join(tmp_path, 'temp.txt') + ' > ' +
                    os.path.join(tmp_path, 'file_list.txt'))

        working_path = os.path.join(os.getcwd(), network)
        prototxt_file = os.path.join(os.getcwd(), network, network + '.prototxt')
        pre_trained_model_file = os.path.join(os.getcwd(), network, os.path.basename(DICT_MODELS[network][0]))

        # create working path if it does not exist
        if not os.path.exists(working_path):
            os.makedirs(working_path)
        # create prototxt if does not exist
        if not os.path.isfile(prototxt_file):
            DICT_MODELS[network][2](prototxt_file, caffe_path, tmp_path)
        # download and set imagenet mean if does not exist
        if not os.path.isfile(os.path.join(caffe_path, 'data/ilsvrc12/imagenet_mean.binaryproto')):
            get_imagenet_mean(caffe_path)
        # download pre trained model if does not exist
        if not os.path.isfile(pre_trained_model_file):
            run_command('wget -P ' + working_path + ' ' + DICT_MODELS[network][0])

        run_command(os.path.join(caffe_path, 'build/tools/extract_features.bin') + ' ' + pre_trained_model_file +
                    ' ' + prototxt_file + ' ' + DICT_MODELS[network][1] + ' ' + os.path.join(tmp_path, 'features') +
                    ' ' + str(number_files) + ' leveldb ' + GPU_CPU, debug=True)

        from_leveldb_to_txt(os.path.join(tmp_path + 'features'),
                            os.path.join(tmp_path + 'feat.txt'), os.path.join(tmp_path + 'key.txt'))

        create_final_files(os.path.join(tmp_path + 'feat.txt'), os.path.join(tmp_path + 'key.txt'),
                           os.path.join(tmp_path, 'temp.txt'),
                           os.path.join(output_path, network + '_features.txt'),
                           number_files)
        shutil.rmtree(tmp_path)
    else:
        print 'No features extracted!'
        print network + '_features.txt already exists.'


if __name__ == "__main__":
    main()
