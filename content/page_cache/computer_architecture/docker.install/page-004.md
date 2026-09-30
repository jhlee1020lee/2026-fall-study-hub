---
course: "computer_architecture"
source_pdf: "Docker.Install.pdf"
pdf_page: 4
source_url: "https://jhlee1020lee.github.io/2026-fall-study-hub/materials/computer_architecture/Docker.Install.pdf"
generated_at: "2026-09-30T14:34:12Z"
---
Environment Setup
1. Install Docker (Ubuntu)

  Install Docker Engine and add yourself to the docker group:
    $ curl -fsSL https://get.docker.com | sudo sh
    $ sudo usermod -aG docker $USER

  On WSL, the script prints a warning and waits ~20 seconds. Just wait.

  Re‐open the shell (exit, then run wsl again), and verify:
    $ docker run hello-world
