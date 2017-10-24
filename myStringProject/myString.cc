//***************************************************************
// Implementation file for myString class - myString.h
// Briana Smith
// Feb 8, 2017
//
// This program emulates the c++ string class. Takes a char or c-string
// and converts it into myString.
// Operators: =
// Constructors: default, const char*, const char&
// Member functions: length, at, substring, erase, insert, find
// Non-member function: getLine
//
// This program could benefit from a resize function, and adding more
// operators such as << and >>.
//***************************************************************

#include "myString.h"

//*****************************************************
/// default constructor   when you ask for the length it HAS to say 0
//*****************************************************
myString::myString()
   : len{0}, arrPtr{nullptr}
{}

//*****************************************************
/// converts c-string to myString
//*****************************************************
myString::myString(const char* p) 
{
   len = 0;
   while(p[len]!='\0')
   {
      len++;
   }

   arrPtr = new char[len];

   for(int i=0;i<len;i++)
   {
      *(arrPtr+i) = *(p+i);
   }
}

//*****************************************************
/// converts char to myString
//*****************************************************
myString::myString(const char& p)
{
   len=1;
   arrPtr = new char[len];
   *(arrPtr+0) = p;
}

//*****************************************************
/// deep copy constructor
//*****************************************************
myString::myString(const myString& x)
: len{x.len}
{
   arrPtr = new char[x.len];
   for(int i=0; i<len; i++)
   {
      arrPtr[i]=x.arrPtr[i];
   }  
}

//*****************************************************
/// assignment operator for =
//*****************************************************
myString& myString::operator=(const myString& M)
{
   if (this != &M)
   {
      delete[] arrPtr;
      arrPtr = nullptr; //added in tutorial
      len = M.len;
      arrPtr = new char[len];
      for(int i=0; i<len; i++)
      {
	       *(arrPtr+i) = *(M.arrPtr+i); //arrPtr[i] = M.arrPtr[i];
      }
   }
   return *this;
}

//*****************************************************
/// destructor
//*****************************************************
myString::~myString()
{
   delete[] arrPtr;
   arrPtr = nullptr;
}

//*****************************************************
/// length
/// Returns the length of the current myString
//*****************************************************
int myString::length()const
{
   return len;
}

//*****************************************************
/// at
/// Returns a character from myString at int i
/// r-value version
//*****************************************************
const char& myString::at(int i)const
{
   assert(i>=0 && i<len);
   return *(arrPtr+i); //return arrPtr[i];
}

//*****************************************************
/// at
/// Changes a character in myString at i
/// l-value version
//*****************************************************
char& myString::at(int i)
{
   assert(i>=0 && i<len);
   return *(arrPtr+i); //return arrPtr[i];
}

//*****************************************************
/// Substring
/// Returns a substring of the current string starting
/// at index k, and of length n
//*****************************************************
myString myString::substr(int k, int n)const
{
   myString temp;
   temp.len=n;
   temp.arrPtr = new char[n];

   assert(n>=0 && n<=len); //allows user to get a substr of 0 characters
   assert(k>=0 && k<=len);
   
	  
   int j = 0;
   for(int i=k; i<k+n; i++)
   {
      temp.arrPtr[j] = *(arrPtr+i);
      j++;
   }

   return temp;
}

//*****************************************************
/// Erase
/// Erases part of the myString, starting at index k,
/// and continuing for length n
//*****************************************************
myString& myString::erase(int k, int n)
{
   assert(n<=len && n>=0); //allows user to erase 0 characters
   assert(k>=0 && k<=len);
   
   int len1 = this->len-n;
   char *tempPtr = new char[len1];
   
    int j = 0;
    for(int i=0; i<this->len; i++)
    {
       if (i>=k && i<=k+(n-1))
	  continue;

       else
       {
	  *(tempPtr+j) = *(this->arrPtr+i);
	  j++;
       }
    }
    
    delete []this->arrPtr;
    arrPtr = nullptr;
    this->arrPtr= new char[len1];
    this->len = len1;
    this->arrPtr = tempPtr;
    tempPtr = nullptr;

    return *this;
 
    }

//*****************************************************
/// Insert
/// Inserts a substring into a myString starting at index k
//*****************************************************
myString& myString::insert(int k, const myString& s)
{
   assert(k>=0 && k<=len);
   
   int sLen=s.len;
   int thisLength = this->len;
   int newLen = sLen + thisLength; //sLen+(this->len);
   int j=0;
   int g=0;

   char *tempPtr = new char[newLen];
      
   for(int i=0; i<newLen; i++)
   {
      if(i<k || i>k+(sLen-1))
      {
	 *(tempPtr+i) = *(this->arrPtr+g);
	 g++; 
      }

      else if(i>=k && i<=k+(sLen-1))
      {
	 *(tempPtr+i) = *(s.arrPtr+j);
	 j++;
      }
   }
   
   this->len = newLen;
   delete []this->arrPtr;
   this->arrPtr= new char[newLen];
   this->arrPtr = tempPtr;
   tempPtr = nullptr;
   
   return *this;
}
//*****************************************************
/// Find
/// Finds a substring in a myString and returns the index
/// of the first character of that substring
//*****************************************************
int myString::find(const myString& s)const
{
 
   for(int i=0; i<=len-s.len; i++)
   {
      bool match = true;
      for(int j=0; j<s.len;j++)
      {
	 if(s.at(j) != at(i+j))
	    match = false;
      }
      if(match) return i;
   }
   return npos;
}

//*****************************************************
/// friend getLine
/// getline function takes istream, enters into myString
/// returns istream
//*****************************************************
istream& getline(istream& is, myString& s)
{

   char ch;
   int j=0;
   //empty the s
   s.erase(0, s.len);
   
   while (is.get(ch) && ch!='\n')
   {
      //resize s.ptr array
      s.len=j+1;
      //add c to the end
      *(s.arrPtr+j) = ch;
      //update len
      j++;
   }
   return is;
}

