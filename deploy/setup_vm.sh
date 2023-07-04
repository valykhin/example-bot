echo "Install docker dependencies"
sudo apt-get update && \
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release \
    python3-pip \
    jq;

echo "Setup docker repository"
sudo mkdir -p /etc/apt/keyrings && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "Install docker"
sudo apt-get update && \
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

echo "Install docker-compose"
sudo curl -L "https://github.com/docker/compose/releases/download/v2.10.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
sudo chmod +x /usr/local/bin/docker-compose && \
docker-compose --version

echo "Check secrets"
pip3 install yq
cd server
cat ../server/docker-compose.yml | yq '.secrets | .[].file' | xargs ls -la
cd ..
