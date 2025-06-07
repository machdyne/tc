# The Zeitlos SOC/OS

Zeitlos is an open-source project designed to bring Timeless Computing to life. It consists of two key components:

- **Zeitlos SOC (System-on-a-Chip)**: A hardware design that integrates a RISC-V CPU, GPU, and other essential subsystems onto a single FPGA.
- **Zeitlos OS (Operating System)**: A lightweight, open-source operating system tailored for timeless applications.

This combination creates a powerful yet simple ecosystem for users of all skill levels.

## Motivation

### Simplicity and Minimalism

   - **Linux** is flexible and can be adapted to many use cases, but it also comes with a lot of complexity. The sheer size and scope of Linux (and the software that runs on it) can make it harder to understand, maintain, and secure.
   - **Zeitlos** is designed from the ground up as a minimal, single-user operating system tailored for timeless applications. Its simplicity makes it easier to understand, audit, and control—perfect for users who want a distraction-free environment focused on specific tasks like reading, writing, or education.

### Customization for Timeless Computing
   - Linux is designed to be a general-purpose OS that can run a wide variety of applications. While this is great for versatility, it often introduces unnecessary complexity and resource overhead for users who only need basic functionality.
   - Zeitlos is built specifically for FPGA-based computers and their unique strengths (like reconfigurable hardware). It’s optimized for timeless computing use cases, such as:
     - Running lightweight, distraction-free applications.
     - Supporting retro or custom computing environments.
     - Providing a stable, secure platform that’s resistant to bloatware or unnecessary updates.

### Longevity and Future-Proofing
   - Linux (and most modern operating systems) are designed with the assumption of constant evolution and improvement. While this is great for innovation, it can also lead to compatibility issues over time as hardware and software evolve.
   - Zeitlos aims to create a system that’s not just modern but also timeless—designed to remain relevant and functional for decades. Its modular design allows for incremental improvements while maintaining backward compatibility with classic computing paradigms.

### Security Through Simplicity
   - Modern Linux distributions are secure, but they’re also complex. Complexity introduces potential vulnerabilities and makes it harder to audit the system for security flaws.
   - Zeitlos is designed with a focus on simplicity and minimalism, which reduces the attack surface and makes the system easier to secure. Its single-user design (with optional multitasking) also eliminates many of the risks associated with multi-user systems.

### Hardware-Aware Design
   - Linux is hardware-agnostic, which means it can run on a wide variety of devices. However, this flexibility often requires compromises in performance or resource usage.
   - Zeitlos is built specifically for FPGA-based hardware and takes full advantage of the unique capabilities of these systems (e.g., reconfigurable logic, low-power operation). This hardware-aware design allows for optimizations that wouldn’t be possible with a one-size-fits-all OS like Linux.

### Retrocomputing and Customization
   - While Linux can run emulators and support classic computing environments, it often does so in a way that feels layered and indirect.
   - Zeitlos aims to recreate the magic of retro systems (like the Amiga or Macintosh) while adding modern capabilities. Its design borrows from the best ideas of classic computers, making it feel familiar and approachable for users who love retrocomputing or want to experiment with custom hardware.

### Long-Term Vision
   - Linux is a fantastic choice for general-purpose computing, but it’s not designed with the same long-term goals as Machdyne. Our goal is to create systems that will remain useful and relevant for decades—even in scenarios where modern technology might fail or become inaccessible (e.g., in a survival computing context).
   - Zeitlos is part of this vision, offering a lightweight, secure, and customizable platform that can evolve alongside timeless hardware.

### Conclusion

Linux (and Kakao Linux) will continue to play a role in our ecosystem for users who want the best of both worlds: the simplicity of FPGA hardware paired with the power of a modern OS.

Zeitlos isn’t meant to replace Linux or other operating systems; it’s designed to fill a specific niche. For users who want a simple, secure, and long-term-focused computing experience on FPGA-based hardware, Zeitlos offers something that Linux just can’t match in terms of customization, minimalism, and hardware integration.

## Design Goals

The Zeitlos SOC/OS project was designed with a specific set of goals in mind to create a system that is both functional and enduring. These goals guide the development process and ensure that the resulting system meets the needs of users who value simplicity, security, and longevity.

### Minimalistic Design
- **Simplicity**: The primary goal is to create a simple and understandable operating system that minimizes complexity while still being practical for everyday use.
- **Hardware Integration**: Zeitlos is designed to work seamlessly with FPGA hardware, leveraging the unique capabilities of these devices to provide a responsive and efficient computing environment.

### Hardware-Accelerated Computing
- **FPGA Utilization**: By utilizing FPGAs, Zeitlos aims to deliver high performance without the need for traditional CPUs or GPUs. This approach allows for hardware-accelerated tasks, which can be particularly beneficial for specific applications.
- **Custom GPU**: The inclusion of a custom 2D "GPU" with sprite support and multiple video modes ensures that the system can handle graphical operations efficiently.

### Multitasking and Resource Management
- **Preemptive Multitasking**: The OS kernel is designed to support preemptive multitasking, allowing for smooth operation of multiple tasks without the overhead of virtual memory or an MMU. This makes the system lightweight yet capable.
- **Kernel Language**: The kernel is written in C, ensuring compatibility and ease of understanding, while applications can be developed in both C and Scheme (a Lisp dialect), offering flexibility for different use cases.

### User-Centric Design
- **Ease of Use**: Despite its technical underpinnings, Zeitlos is designed to be user-friendly. The interface is intuitive, with a focus on usability that makes it accessible even to those who are not deeply familiar with computing systems.
- **Support for Applications**: The system supports both new applications tailored to its environment and existing ones through emulation or additional hardware resources, ensuring a broad range of functionality.

### Security and Longevity
- **Security**: By focusing on simplicity and minimizing unnecessary features, Zeitlos inherently reduces the attack surface, making it more secure compared to complex modern operating systems.
- **Enduring Relevance**: The design aims for long-term relevance, ensuring that the system remains functional and useful even as technology evolves. This is crucial for applications where longevity and reliability are paramount.

### Modularity and Extensibility
- **Modular Design**: The system is built with modularity in mind, allowing for future expansion and adaptation to new hardware or requirements without compromising existing functionality.
- **Upgradability**: Users should be able to upgrade or replace components as needed, ensuring that the system can evolve alongside technological advancements.

### Open Source Philosophy
- **Transparency**: By being open-source, Zeitlos fosters transparency and trust. This allows users and developers to review the code, contribute improvements, and ensure the system remains secure and reliable.
- **Collaboration**: The open-source nature encourages collaboration within the community, allowing for a diverse range of contributions that can enhance the system over time.

### User Experience
- **Graphical Interface**: A mouse and keyboard-based interface provide an intuitive way to interact with the system, making it accessible even to those who are not deeply technical.
- **Documentation**: Comprehensive documentation, including this book, will be integrated into the OS, ensuring that users can easily understand how to use and maintain their systems.

### Sustainability and Accessibility
- **Low Power Consumption**: The design considerations include low power consumption, making the system suitable for environments where energy resources may be limited or where sustainability is a priority.
- **Accessibility**: The system aims to be accessible to a wide range of users, including those in regions with limited access to modern technology, ensuring that computing remains affordable and practical.

### Future-Proofing
- **Adaptability**: The modular design ensures that the system can adapt to future hardware advancements while maintaining its core functionality. This adaptability is crucial for ensuring that the system remains relevant over the long term.
- **Preservation of Usefulness**: By focusing on timeless applications, Zeitlos aims to preserve its usefulness even in scenarios where modern computing infrastructure may be unavailable or compromised.

### Community and Collaboration
- **Community Support**: The open-source model encourages a community-driven approach to development, ensuring that the system benefits from a wide range of perspectives and expertise.
- **Feedback Integration**: The design process incorporates feedback from users and contributors, allowing for continuous improvement and refinement of the system.

### Summary

In summary, the Zeitlos SOC/OS is designed with a focus on simplicity, security, and longevity, aiming to provide a computing environment that is both functional today and enduring into the future. Its modular and open-source nature ensures that it can evolve alongside technological advancements while remaining accessible to a wide range of users.

## System Overview

The Zeitlos system is built around the following core components:

1. RISC-V CPU: The heart of the system, designed for efficiency and long-term reliability.
2. Custom GPU: A hardware-accelerated "blitter" for fast graphics rendering, supporting multiple resolutions and modes.
3. FPGA-Based Hardware: Compatible with a variety of FPGA boards, ensuring flexibility and adaptability.

## The Zeitlos Kernel

The kernel is the core of the operating system, written in C for reliability and performance. It provides essential services like:

- Process management
- Memory allocation
- Device drivers
- Interrupt handling
- Message handling

Zeitlos uses a preemptive multitasking model to handle multiple tasks efficiently while keeping resource usage low.

## User-Friendly Design

The Zeitlos OS is designed with the end-user in mind:

- Graphical Interface: A clean, intuitive interface for interacting with applications.
- Built-in Tools: Pre-installed utilities for system management and development.
- Scripting Support: Built-in Scheme interpreter for advanced users.

## Getting Started

To use Zeitlos, you'll need:

1. An FPGA board (e.g., Machdyne FPGA computers or a development board).
2. The latest version of the Zeitlos OS.

## Get Involved

Zeitlos is under active development. Find more information at:

\url{https://zeitlos.org}

and in the GitHub repo:

\url{https://github.com/machdyne/zeitlos}.
