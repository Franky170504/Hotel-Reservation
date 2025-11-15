FROM jenkins/jenkins:lts

# Switch to root user to install dependencies
USER root

# Install prerequisites and Docker

RUN apt-get update -y && \
    # Install packages needed to add a repo
    apt-get install -y ca-certificates curl gnupg && \
    \
    # Create the directory for GPG keys
    install -m 0755 -d /etc/apt/keyrings && \
    \
    # Download and de-armor Docker's GPG key
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
    \
    # Set permissions for the key
    chmod a+r /etc/apt/keyrings/docker.gpg && \
    \
    # Add the Docker repository, using the 'trixie' repo to match your base image
    echo \
      "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
      trixie stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
    \
    # Update apt lists and install Docker
    apt-get update -y && \
    apt-get install -y docker-ce docker-ce-cli containerd.io && \
    \
    # Clean up
    apt-get clean

    # Add Jenkins user to the Docker group (create if it doesn't exist)

RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Create the Docker directory and volume for DinD

RUN mkdir -p /var/lib/docker

VOLUME /var/lib/docker

# Switch back to the Jenkins user

USER jenkins