#include "stdafx.h"
#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <stdio.h>
#include <fstream>
#include <string>
#include <windows.h>
#include <winreg.h>
#include <tchar.h>
#include <process.h>

using namespace std;

ifstream in("test.txt");

// estimate time
LARGE_INTEGER StartingTime, EndingTime, ElapsedMicroseconds, TotalElapsedMicroseconds;
LARGE_INTEGER Frequency;

//openkey 
HKEY key;

//query 
DWORD type;
DWORD sizes;
char buffer[1024];

//setvalue 
char newdata[16] = "new data";

//showkey
DWORD i = 0;
TCHAR keyName[1024];

//showvalue
TCHAR valueName[1024];
DWORD valueSize = 1024;
LPSTR saveData;

//event handler
DWORD dwThreadID = 1;
unsigned threadId;
HANDLE hHandle;

//file operation
HANDLE fHandle;
TCHAR Strings[1];
DWORD fileresult;


class Sources {

public:

	int open_key() {

		RegOpenKeyEx(HKEY_CLASSES_ROOT, "zune", 0, KEY_ALL_ACCESS, &key);

		return 0;
	}

	int close_key() {

		RegCloseKey(key);

		return 0;
	}

	int read_value() {

		RegQueryValueExA(key, "aaa", 0, &type, (LPBYTE)buffer, &sizes);

		return 0;

	}

	int write_value() {

		RegSetValueEx(key, "aaa", 0, REG_SZ, (const unsigned char *)newdata, (strlen(newdata) + 1));

		return 0;
	}

	int show_key() {

		RegEnumKey(key, i, keyName, 512);

		return 0;
	}

	int show_value() {

		RegEnumValue(key, i, valueName, &valueSize, NULL, NULL, (LPBYTE)saveData, NULL);

		return 0;
	}


	int create_key() {

		RegCreateKeyEx(key, "**", 0, NULL, REG_OPTION_NON_VOLATILE, KEY_ALL_ACCESS, NULL, &key, NULL);

		return 0;

	}

	int delete_key() {

		RegDeleteKey(key, "**");

		return 0;
	}

	int delete_value() {

		RegDeleteValue(key, "aaa");

		return 0;
	}

	int file_operation() {
		fHandle = CreateFile(_T("file.txt"), GENERIC_READ, 0, NULL, CREATE_ALWAYS, 0, NULL);
		ReadFile(fHandle, Strings, sizeof(TCHAR) * 2, &fileresult, NULL);
		return 0;
	}


	int main_operation() {

		read_value();
		file_operation();

		return 0;
	}

};

Sources s;


class Duplication {

public:

	int p1_open_close() {

		for (int i = 0; i < 9954; i++) {
			s.open_key();
			s.main_operation();
			s.close_key();
		}



		return 0;

	}

	int p3_open_read_value_close() {

		for (int i = 0; i < 9999; i++) {
			s.open_key();
			s.read_value();
			s.main_operation();
			s.close_key();
		}

		return 0;

	}

	int p5_open_write_value_close() {

		for (int i = 0; i < 9996; i++) {
			s.open_key();
			s.write_value();
			s.main_operation();
			s.close_key();
		}

		return 0;

	}


	int p6_open_show_key_close() {

		for (int i = 0; i < 10000; i++) {
			s.open_key();
			s.show_key();
			s.main_operation();
			s.close_key();
		}

		return 0;

	}

	int p7_open_show_value_close() {

		for (int i = 0; i < 9999; i++) {
			s.open_key();
			s.show_value();
			s.main_operation();
			s.close_key();
		}

		return 0;

	}

	int p9_show_write_key() {

		for (int i = 0; i < 13888; i++) {
			s.show_key();
			s.main_operation();
		}

		return 0;
	}


	int p10_read_write_value() {

		for (int i = 0; i < 9504; i++) {
			s.read_value();
			s.main_operation();
		}

		return 0;
	}

	int p11_show_write_value() {

		for (int i = 0; i < 12904; i++) {
			s.show_value();
			s.main_operation();
		}

		return 0;
	}

	int p12_create_delete_key() {

		s.open_key();

		for (int i = 0; i < 10000; i++) {
			s.create_key();
			s.delete_key();
			s.main_operation();

		}

		s.close_key();

		return 0;

	}

	int p13_create_delete_value() {

		s.open_key();

		for (int i = 0; i < 9999; i++) {
			s.write_value();
			s.delete_value();
			s.main_operation();
		}

		s.close_key();

		return 0;

	}
};


class Deduplication {

public:

	int p1_open_close() {

		for (int i = 0; i < 1659; i++) {
			s.open_key();
			for (int i = 0; i < 6; i++) {
				s.main_operation();
			}
			s.close_key();
		}

		return 0;

	}

	int p3_open_read_value_close() {

		for (int i = 0; i < 909; i++) {
			s.open_key();
			for (int i = 0; i < 11; i++) {
				s.read_value();
				s.main_operation();
			}
			s.close_key();
		}
		return 0;
	}

	int p5_open_write_value_close() {

		for (int i = 0; i < 1666; i++) {
			s.open_key();
			for (int i = 0; i < 6; i++) {
				s.write_value();
				s.main_operation();
			}
			s.close_key();
		}
		return 0;
	}

	int p6_open_show_key_close() {

		for (int i = 0; i < 5000; i++) {
			s.open_key();
			for (int i = 0; i < 2; i++) {
				s.show_key();
				s.main_operation();
			}
			s.close_key();
		}
		return 0;
	}

	int p7_open_show_value_close() {

		for (int i = 0; i < 3333; i++) {
			s.open_key();
			for (int i = 0; i < 3; i++) {
				s.show_value();
				s.main_operation();
			}
			s.close_key();
		}

		return 0;

	}


	static unsigned __stdcall event_handler_show_key(void* pArguments) {

		DWORD regFilter = REG_NOTIFY_CHANGE_ATTRIBUTES | REG_NOTIFY_CHANGE_LAST_SET | REG_NOTIFY_CHANGE_NAME | REG_NOTIFY_CHANGE_SECURITY;
		HANDLE hEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
		LRESULT result = RegNotifyChangeKeyValue(key, true, regFilter, hEvent, true);

		while (WaitForSingleObject(hEvent, INFINITE) == 0) {
			s.show_key();
		}

		CloseHandle(hEvent);
		return 0;

	}

	int p9_show_write_key() {
		for (int i = 0; i < 6944; i++) {
			hHandle = (HANDLE) _beginthreadex(NULL, 4096, event_handler_show_key, NULL, 0, &threadId);
			for (int i = 0; i < 2; i++) {
				s.main_operation();
			}
			ExitThread(threadId);
		}

		return 0;

	}

	static unsigned __stdcall event_handler_read_value(void* pArguments) {

		DWORD regFilter = REG_NOTIFY_CHANGE_ATTRIBUTES | REG_NOTIFY_CHANGE_LAST_SET | REG_NOTIFY_CHANGE_NAME | REG_NOTIFY_CHANGE_SECURITY;
		HANDLE hEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
		LRESULT result = RegNotifyChangeKeyValue(key, true, regFilter, hEvent, true);

		while (WaitForSingleObject(hEvent, INFINITE) == 0) {
			s.read_value();
		}

		CloseHandle(hEvent);
		return 0;

	}

	int p10_read_write_value() {
		for (int i = 0; i < 1188; i++) {
			hHandle = (HANDLE)_beginthreadex(NULL, 4096, event_handler_read_value, NULL, 0, &threadId);
			for (int i = 0; i < 8; i++) {
				s.main_operation();
			}
			ExitThread(threadId);
		}
		return 0;

	}

	static unsigned __stdcall event_handler_show_value(void* pArguments) {

		DWORD regFilter = REG_NOTIFY_CHANGE_ATTRIBUTES | REG_NOTIFY_CHANGE_LAST_SET | REG_NOTIFY_CHANGE_NAME | REG_NOTIFY_CHANGE_SECURITY;
		HANDLE hEvent = CreateEvent(NULL, FALSE, FALSE, NULL);
		LRESULT result = RegNotifyChangeKeyValue(key, true, regFilter, hEvent, true);

		while (WaitForSingleObject(hEvent, INFINITE) == 0) {
			s.show_value();
		}

		CloseHandle(hEvent);
		return 0;

	}

	int p11_show_write_value() {
		for (int i = 0; i < 6452; i++) {
			hHandle = (HANDLE)_beginthreadex(NULL, 4096, event_handler_show_value, NULL, 0, &threadId);
			for (int i = 0; i < 2; i++) {
				s.main_operation();
			}
			ExitThread(threadId);
		}
		return 0;

	}

	int p12_create_delete_key() {

		s.open_key();

		for (int i = 0; i < 5000; i++) {
			s.create_key();
			for (int i = 0; i < 2; i++) {
				s.main_operation();
			}
			s.delete_key();
		}

		s.close_key();

		return 0;

	}

	int p13_create_delete_value() {

		s.open_key();

		for (int i = 0; i < 3333; i++) {
			for (int i = 0; i < 3; i++) {
				s.write_value();
				s.main_operation();
			}
		}

		s.delete_value();

		s.close_key();

		return 0;

	}

};


class Multi {

	Duplication a;
	Deduplication b;

public:

	int multi_operation_duplication(int num) {

		for (int i = 1; i <= num; i++) {

			a.p1_open_close();
			a.p3_open_read_value_close();
			a.p5_open_write_value_close();
			a.p6_open_show_key_close();
			a.p7_open_show_value_close();
			a.p9_show_write_key();
			a.p10_read_write_value();
			a.p11_show_write_value();
			a.p12_create_delete_key();
			a.p13_create_delete_value();

		}

		return 0;

	}

	int multi_operation_deduplication(int num) {

		for (int i = 1; i <= num; i++) {

			b.p1_open_close();
			b.p3_open_read_value_close();
			b.p5_open_write_value_close();
			b.p6_open_show_key_close();
			b.p7_open_show_value_close();
			b.p9_show_write_key();
			b.p10_read_write_value();
			b.p11_show_write_value();
			b.p12_create_delete_key();
			b.p13_create_delete_value();

		}

		return 0;

	}

};

int main()
{

	QueryPerformanceFrequency(&Frequency);
	QueryPerformanceCounter(&StartingTime);

	Duplication a;
	Deduplication b;

	//a.p1_open_close();
	//b.p1_open_close();

	//a.p3_open_read_value_close();
	//b.p3_open_read_value_close();

	//a.p5_open_write_value_close();
	//b.p5_open_write_value_close();

	//a.p6_open_show_key_close();
	//b.p6_open_show_key_close();

	//a.p7_open_show_value_close();
	//b.p7_open_show_value_close();

	//a.p9_show_write_key();
	//b.p9_show_write_key();

	//a.p10_read_write_value();
	//b.p10_read_write_value();

	//a.p11_show_write_value();
	//b.p11_show_write_value();

	//a.p12_create_delete_key();
	//b.p12_create_delete_key();

	//a.p13_create_delete_value();
	//b.p13_create_delete_value();


	Multi m;

	//m.multi_operation_duplication(1);
	//m.multi_operation_deduplication(1);

	//m.multi_operation_duplication(5);
	//m.multi_operation_deduplication(5);

	m.multi_operation_duplication(10);
	//m.multi_operation_deduplication(10);

	//m.multi_operation_duplication(15);
	//m.multi_operation_deduplication(15);

	//m.multi_operation_duplication(20);
	//m.multi_operation_deduplication(20);

	QueryPerformanceCounter(&EndingTime);
	ElapsedMicroseconds.QuadPart = EndingTime.QuadPart - StartingTime.QuadPart;

	ElapsedMicroseconds.QuadPart *= 1000000;
	ElapsedMicroseconds.QuadPart /= Frequency.QuadPart;

	printf("Time: %lld microseconds \n", ElapsedMicroseconds.QuadPart);

	system("pause");
	return 0;
}