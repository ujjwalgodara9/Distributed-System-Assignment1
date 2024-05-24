# Distributed Systems Assignment

## Assignment Overview

This repository contains the solutions for the Winter 2024 CSE530 Distributed Systems assignment. The assignment is divided into three parts, each focusing on building a different distributed system component using various technologies:

1. **Online Shopping Platform with gRPC**: Implementing a platform where sellers and buyers interact with a central market using gRPC for communication.
2. **Low-Level Group Messaging Application with ZeroMQ**: Building a messaging application with a central server, groups, and users using ZeroMQ.
3. **YouTube-like Application with RabbitMQ**: Developing a simplified version of a YouTube application with YouTubers, users, and a server using RabbitMQ.

Each part of the assignment comes with detailed specifications and requirements.

## Setup Instructions

### Prerequisites

- Python 3.x
- RabbitMQ (for Part 3)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ujjwalgodara9/Distributed-System
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Components

#### Part 1: Online Shopping Platform (gRPC)

1. Navigate to the `gRPC` directory.
2. Implement the server and client scripts as per the specifications.
3. Run the market (central platform) server script.
4. Run the seller and buyer client scripts.

#### Part 2: Low-Level Group Messaging Application (ZeroMQ)

1. Navigate to the `ZeroMQ` directory.
2. Implement the message server, group, and user scripts as per the specifications.
3. Run the message server script.
4. Run the group and user scripts for testing.

#### Part 3: YouTube-like Application (RabbitMQ)

1. Navigate to the `RabbitMQ` directory.
2. Implement the YouTube server, YouTuber, and User scripts as per the specifications.
3. Run the YouTube server script.
4. Run the YouTuber and User scripts for testing.

### Note

- Ensure RabbitMQ is installed and running for Part 3.
- Make sure to follow the specifications and test thoroughly before submission.

## Additional Notes

- Each component should be implemented with error handling and proper documentation.
- The code should be tested thoroughly and run without errors.
- Ensure to shut down any Google Cloud instances when not in use to conserve credits.
- Refer to the assignment description and resources provided for further details and clarifications.
- https://docs.google.com/document/d/e/2PACX-1vSs74PECKf0OE_GZi5N4soGXrY6v8a1z1pEHLxvZtG0wLAHNcjjg5vi_zj03BKSFYNZI6poat6TJ3v1/pub

---

