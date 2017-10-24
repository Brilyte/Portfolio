//myString.h
//
// Briana Smith
// Feb 8, 2016
//
// This is the header file for the myString class (myString.cc file).

#ifndef MYSTRING_H
#define MYSTRING_H

#include<iostream>
#include<cassert>
using namespace std;

class myString 
{
	public:
	//constructors
		myString(); //default constructor
		myString(const char* p);
		myString(const char&);
		myString(const myString& x); //copy constructor
		myString& operator=(const myString &M); //assignment operator
		~myString();
		friend istream& getline(istream& is, myString& s);
	
	//input and output constructors
		int length()const;
		const char& at(int i)const;
		char& at(int i);
		myString substr(int k, int n)const;
		myString& erase(int k, int n);
		myString& insert(int k, const myString& s);      
		int find(const myString& s)const;
			
	private:
	//data members:  What do we need to keep track of?
		static const int npos= -1;
		int len;
		char *arrPtr;
};

#endif



