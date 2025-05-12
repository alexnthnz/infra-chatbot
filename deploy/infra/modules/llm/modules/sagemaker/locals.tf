locals {
  instance_gpu_count = {
    "ml.g5.xlarge"    = 1
    "ml.g5.2xlarge"   = 1
    "ml.g5.4xlarge"   = 1
    "ml.g5.12xlarge"  = 4
    "ml.g5.48xlarge"  = 8
    "ml.g6.xlarge"    = 1
    "ml.g6.2xlarge"   = 1
    "ml.g6.4xlarge"   = 1
    "ml.g6.12xlarge"  = 4
    "ml.g6.48xlarge"  = 8
    "ml.p4d.24xlarge" = 8
    "ml.p5.48xlarge"  = 8
  }
  num_gpus = local.instance_gpu_count[var.sagemaker_instance_type]
}
