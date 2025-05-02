#!/bin/bash

yum install -y amazon-linux-extras
amazon-linux-extras enable postgresql14
yum clean metadata
yum install -y postgresql
