# Threat Hunter Script

This script monitors local system activity by auditing active processes and inspecting network connections. It identifies processes that are using too many system resources and categorizes established network connections as either internal or external.

## What It Solves

* Detects high CPU usage across running tasks by applying a user-defined threshold.
* Captures ownership details for active processes, handling permission restrictions gracefully.
* Filters network traffic to show only established connections, flagging traffic going outside the local network.

## Technical Choices

* Written in Python 3 for portability and direct execution from the terminal.
* Uses the psutil library to collect real-time system process metrics and active network sockets.
* Uses a 0.2-second sleep interval between process iterations to calculate accurate CPU consumption percentages.
* Uses the built-in ipaddress module to evaluate remote IPs and check whether they match loopback or private subnets.
* Includes exception handling to bypass protected system processes and warns the user when root or administrator privileges are missing.

## Prerequisites

You need Python 3 and the psutil library installed.

Install the required library using pip:

```bash
pip install psutil