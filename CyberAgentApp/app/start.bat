@echo off
cd /d C:\Users\david\Downloads\CyberAgentApp\app
start cmd /k "uvicorn main:app --reload"
