// anagrams.cc
// Briana Smith
// March 8, 2017
// This program takes a list of words and outputs the common
// anagrams, one set of common anagrams per line.
// It ignores words that have no anagrams in the list.

#include<iostream>
#include<string>
#include<algorithm>
#include<map>
#include<vector>

using namespace std;

string signature(const string& w);

int main() {
   string userIn, Sig;
   
   vector<string> sorted;
   map<string, vector<string>> anagrams;
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
   return 0;
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
