IMAGE_NAME="ghcr.io/valykhin/example-bot/core"
CONTEXT=".."
BUILD_OPTIONS="--platform linux/amd64"
IMAGE_VERSION="$1"
if [ -z "$IMAGE_VERSION" ]; then IMAGE_VERSION=$(python version.py); fi


set -x
docker build -f Dockerfile -t ${IMAGE_NAME}:${IMAGE_VERSION} ${BUILD_OPTIONS} ${CONTEXT} && \
docker push "${IMAGE_NAME}:${IMAGE_VERSION}"

