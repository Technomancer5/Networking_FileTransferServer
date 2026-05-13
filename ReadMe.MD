 # Overview

Purpose:
To increase my undertanding of how software/code works behind the scenes on networks.  I will use this software to 'hack' unencrypted files with my Flipper Zero and learn about the vulnerabilities on my network.  I will then use that information to further harden my network and ensure any of my successful previous 'hacking' is no longer possible.

About:
This program allows me to move files from one computer on my network to another, using my Linux, Windows, or Mac.  It is also more intuitive to use than command line and more robust than just having a shared folder on my network.

Notes:
Files are currently sent unencrypted, do NOT use for sensitive data.
You must have Python installed on the PCs to run this program.
Currently you can only send files that are located in the same folder as the python script due to an oversight, this will be corrected on a later version.
You may want to replace the IP addresses, names and OS in the BUILT_IN_PEERS located in the Configuration.

Instructions:
On the PC you are sending files from, open command line and navigate to the directory/folder with the script and files you want to send.

Then start the program on that PC by entering: 
python NetFileMaster.py 
Or for Mac: python3 NetFileMaster.py

Repeat those steps on your other PC on the network.

On the PC you are sending files from you will follow the prompts and select the option of the computers IP address you are sending files to or use option 'B' to manually enter the IP.
Then the destination folder from the list or manually enter it using option 'M'.
Then choose the option for the files you are sending to send it to the destination folder.

The file(s) will send and restart the program, use ctrl + c to quit.
Don't forget to quit the program on both PCs when finished.

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running (you will need to show two pieces of software running and communicating with each other) and a walkthrough of the code.}

[Software Demo Video](https://youtu.be/QOfKSSRRRBo)


# Network Communication

This can currently be used for client/server or peer-to-peer but not recommended to run as Client/server until a later version with encryption.
It also currently will leave the port open and may be vulnerable to bad actors if they gain access to your network. 

Protocol:
I used TCP because it is a reliable protocol that ensures every "packet" of data arrives in the correct order and without errors. Unlike UDP, if a packet is lost during transmission, TCP automatically requests it again, which is essential for ensuring that files do not end up corrupted.
This choice is also critical for my chunking strategy; by sending files in 4096-byte segments, TCP's error-checking ensures each piece is reassembled correctly on the receiving end.
TCP will also allow me to use the standard ssl library which is designed to wrap around a reliable TCP stream to create the secure tunnel for data when I updgrade the program to be used outside of my network.

Port:
I am currently using port 65432 but may change this.

Message Format:
I am using Binary Chunks to break down the file data in to 4096-byte chunks


# Development Environment

Software/Tools used:
VScode for the coding and Github for version control and to push and pull my code between my devices
Google LM Notebook was used to organize the project and research the project.
I also used Kate (like notepad) on my Linux machine for notes on tracking project time and simple data such as commands or IP addresses.
When I got started I used my Windows Server 2022 to easily share my code before I finished setting up VScode and github on my other PCs.
I also used Gemini for any research I did not want saved to my project in Google LM Notebook.
Tested code on my Mac Mini, Linux Garuda Laptop and my Windows 11 Desktop. 

I used Python for my programming language.
I used the libraries: Socket, OS, threading, ssl, tqdm, argparse, Click, Typer, pypager, spaCy, node-llama-cpp and ora.

# Useful Websites

{Make a list of websites that you found helpful in this project}
* [Google LM Notebook] (https://notebooklm.google.com/notebook/7621d8ae-8b88-4630-99ab-d4660fa35a02)
* [Python Articles] (https://www.tutorialspoint.com/articles/category/python)
* [Command Line Interface Guidelines] (https://clig.dev/)
* [Newsdata.io] (https://newsdata.io/blog/deploying-windows-server-2022-installation-configuration-and-initial-setup-guide/)
* [Microsoft Learn] (https://learn.microsoft.com/en-us/windows-server/get-started/hardware-requirements)

# Future Work

{Make a list of things that you need to fix, improve, and add in the future.}
* Item 1: I need to do stress testing and testing to try to break it to enhance the performance, in addition to adding some personal touches.
* Item 2: I want to add options to go back a menu and an option to choose another destination folder.
* Item 3: Due to an oversight the files being sent need to reside in the same folder as the script in order for it to run.
* Item 4: I will be adding encryption.
* Item 5: I will be adding a GUI.
* Item 6: I want to setup a secure tunnel to use outside my network.