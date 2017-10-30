// perm.cc
// CPSC 2620 Assignment 6 - Question 2
// Briana Smith
//
// This program takes n integers into an array and prints every possible
// permutation of their sequence: (1,2....n).

#include<iostream>
using namespace std;

void print_perm(int A[], int n, int current);

int main()
{
   int userSize;
   
   do{
      cout<<"Enter n (0 to quit): "<<endl;
      cin>>userSize;
      int A[userSize];
      for(int i=0; i<userSize;i++)
	 A[i] = i+1;
      int current = 0;
      print_perm(A, userSize, current);
   }
   while(userSize>0);
   
   return 0;
}

// print_perm
// This function takes the array, n(the end of the sequence), and the start
// of the array to print every permutation of their sequence.
void print_perm(int A[], int n, int current)
{
   if(current==n)
   {
      for(int j=0; j<n; j++)
	 if(j<n-1)
	    cout<<A[j]<<",";
	 else
	    cout<<A[j];
      
      cout<<endl;
   }
   
   else
   {
      for(int i=current; i<n; i++)
      {
	 swap(A[current],A[i]);
	 print_perm(A,n,current+1);
	 swap(A[current],A[i]);
      }
   }
}
