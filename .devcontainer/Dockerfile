ARG DEVCONTAINER_ROS_IMAGE_TAG=jazzy
FROM ros:${DEVCONTAINER_ROS_IMAGE_TAG}

# The Jazzy base image already ships a non-root 'ubuntu' user (UID/GID 1000) in the sudo group.
ARG USERNAME=ubuntu

RUN echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME} \
    && echo 'source /opt/ros/${ROS_DISTRO}/setup.sh' >> /home/${USERNAME}/.bashrc \
    && mkdir -p /home/${USERNAME}/infield_robotics_ws/src \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}

RUN apt-get update \
    && apt-get install -y \
        python3-colcon-common-extensions \
        ros-${ROS_DISTRO}-tf-transformations \
        ros-${ROS_DISTRO}-foxglove-bridge \
    && rm -rf /var/lib/apt/lists/*

# ********************************************************
# * Anything else you want to do like clean up goes here *
# ********************************************************

# [Optional] Set the default user. Omit if you want to keep the default as root.
USER $USERNAME
