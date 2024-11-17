# Gallery App

## Overview
The Gallery App is a fully functional photo storage and management application built using Flask, HTML, CSS, and integrated with Google Cloud Platform services. It allows users to securely upload, view, manage, and download their photos, with metadata for each image displayed for better organization. The app ensures data privacy by restricting access to user-specific data.

## Features
- **User Authentication:** Secure login and registration using Google Firebase for user authentication and credential encryption.
- **Photo Management:** 
  - Upload photos directly to your account.
  - View and manage photos on your personalized dashboard.
  - View metadata for each photo, such as upload date, dimensions, and file size.
  - Download or delete photos as needed.
- **Cloud Integration:** 
  - Photos are stored as BLOBs in Google Cloud Storage.
  - Metadata is managed using Google Datastore.
- **Cross-Platform Access:** Users can access their photo gallery from any device or browser.

## Architecture
The app uses the following components:
1. **Frontend:** Built with Flask templates using HTML and CSS for a responsive and user-friendly interface.
2. **Backend:** Developed in Python using Flask for handling requests and managing user sessions.
3. **Cloud Services:**
   - Google Cloud Storage for storing photos securely.
   - Google Firebase for user authentication.
   - Google Cloud Datastore for managing photo metadata.
4. **Hosting:** The application is deployed on Google Cloud Platform using Cloud Run.


### How to Use
1. **Sign Up / Login:**
   - Register as a new user by providing your email and a secure password.
   - Existing users can log in with their credentials.
2. **Upload Photos:**
   - Click on the "Choose File" button to select a photo from your device.
   - Click "Upload" to add the photo to your gallery.
3. **Manage Photos:**
   - View photos in your dashboard.
   - Click on a photo to view its metadata.
   - Use the "Download" or "Delete" buttons to manage your photos.
