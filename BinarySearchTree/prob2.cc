// prob2.cc
// Briana Smith
// April 4, 2017
// Assignment 6 - Question 1
// This program takes a list of words and outputs the common
// anagrams, one set of common anagrams per line.
// **It ignores words that have no anagrams in the list.
//
// Updated version uses custom BST instead of STL map

#include<iostream>
#include<string>
#include<algorithm>
//#include<map>
#include "BST.h"
#include<vector>

using namespace std;

string signature(const string& w);
void print(const string&, vector<string>&);

int main() {
   string userIn, Sig;
   
   vector<string> sorted;
   //map<string, vector<string>> anagrams;
   BST anagrams;
   
   cout<<"Enter anagrams in uppercase, hit enter between each."<<endl
       <<"Enter EXIT-PROGRAM to quit."<<endl;
   cin>>userIn;
  
   while(/*!cin.eof() ||*/ userIn!="EXIT-PROGRAM")//eof option for file entry
   {
      Sig = signature(userIn);
      anagrams[Sig].push_back(userIn);
      //Sig is key, push userIn string to vector
      cin>>userIn;
   }
   cout<<endl;
   //traverse and print BST here:
   anagrams.traverse(print);
   
   /*
   //Assignment 4 code for reference:
   for(auto it=anagrams.cbegin(); it!=anagrams.cend(); ++it)
   {
      if(it->second.size()>1) //if there is more than one anagram
      {
	 cout<<"Anagrams: "<<endl;
	 for(auto vit=it->second.begin(); vit!=it->second.end(); ++vit)
	 {
	    cout<<*vit<<" "; //dereference vector
	 }
	 cout<<endl<<endl;
      }
    }
   */
   return 0;
}

//print
//This function prints the BST anagrams
//If no other anagram exists (just a single word) it does not print that word
void print(const string& key, vector<string>& val)
{
   if(val.size()>1)
   {
      cout<<"Anagrams:"<<endl;
      for(size_t i=0;i<val.size();i++)
      {
	 cout<<val[i]<<" ";
      }
      cout<<endl<<endl;
   }
}

//signature
//This function returns sorted string w, arranges its chars in
//alphabetical order
string signature(const string& w)
{
   string sig = w;
   sort(sig.begin(), sig.end());
   return sig;
}
