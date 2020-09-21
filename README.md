# Webpage
Webpage for presentation of work done during ITSP 2019-20

## Getting Started

* Clone this to your PC
  ```
  git clone https://github.com/kenzz17-ITSP/webpage.git
  ```
  (or download the zip file from the top right green button)
  
* Virtual Environment (Optional)
  ```
  pip3 install virtualenv
  ```
  Create a virtual env in the same folder where you stored the web page folder
  
  To create a virtual env:
  ```
  virtualenv env
  ```
  Activate virtual env
  ```
  source env/bin/activate
  ```
* Unzip drive-download-20200628T124658Z-001.zip and rename the following files.
  ```
  1. model2.h5 -> model.h5
  2. model2.json -> model.json
  3. tokenizefinal.p -> tokenizer.p
  ```
  After renaming, replace all the files already present in the cloned folder with the same names as above with these new files (take help of tree.txt to locate all).
  
* Install requirements, suppose your folder name is abc
  ```
  cd abc
  pip3 install -r requirements.txt
  ```
  
* Run Django server
  ```
  python3 manage.py runserver
  ```
Check tree.txt for files to be kept inside model directory

## Model Training
The model was trained in the following colab notebook : 
https://colab.research.google.com/drive/128ZkorEyBc-Bnkgw_CiD2uKlg8brc-Ra?usp=sharing
