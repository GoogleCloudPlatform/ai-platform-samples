# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
variable "project_id" {
  type        = string
  description = "Project ID"
}

variable "credentials_file" {}

variable "region" {
  type        = string
  default     = "us-west1"
  description = "The region that this terraform configuration will use."
}

variable "location" {
  type        = string
  default     = "us-west1-b"
  description = "The zone that this terraform configuration will use."
}

variable "instance_type" {
  type        = string
  default     = "n1-standard-1"
  description = "The instance_type that this terraform configuration will use."
}

variable "gpu_type" {
  type        = string
  default     = "nvidia-tesla-t4"
  description = "The GPU type: https://cloud.google.com/gpu"
}

variable "gpu_count" {
  type        = number
  default     = 1
  description = "The GPU number"
}
