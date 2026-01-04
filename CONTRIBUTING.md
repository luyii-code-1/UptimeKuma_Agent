# Contributing Guide

[English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING_zh-CN.md)

Thank you for your interest in the UptimeKuma Agent project! This guide will help you understand how to contribute to the project. 

## Code Submission Requirements

### Code Quality Standards
- **No AI-Generated Code**: Submitted code must be written by humans or reviewed by humans. Do not use AI tools to generate entire files or large code segments.
- **Reasonable Comments**: Code should include appropriate comments explaining complex logic, function purposes, and key steps. Comments should be clear, concise, and in English or Chinese.

### CI/CD Checks
Before submitting code, ensure your changes pass the following automated checks:
- **PyLint Score**: Code must achieve a PyLint score greater than 7. PyLint checks code quality, style, and potential errors.
- **CodeQL Scan**: Code must pass CodeQL security scanning to ensure no security vulnerabilities.

### Review Process
- After submitting a Pull Request (PR), CI will automatically run the above checks.
- If CI passes, the code will enter the Copilot review phase. Copilot will review the overall quality, compliance, and best practices of the code,after that, a member of the contributors will review it.

## How to Contribute
1. Fork this repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## Contact Us
If you have any questions, please reach out to us through Issues or Discussions.