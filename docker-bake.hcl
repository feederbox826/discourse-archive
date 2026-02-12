
// variables
variable "OWNER_NAME" {
  type = string
  default = "feederbox826"
}

variable "IMAGE_NAME" {
  type = string
  default = "discourse-archive"
}

group "default" {
  targets = ["alpine"]
}

target "alpine" {
  context = "."
  dockerfile = "Dockerfile"
  tags = [
    "ghcr.io/${OWNER_NAME}/${IMAGE_NAME}:latest",
  ]
  platforms = ["linux/amd64", "linux/arm64"]
  cache-to = [{ type = "gha", mode = "max" }]
  cache-from = [{ type = "gha" }]
}