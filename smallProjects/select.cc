// select.cc
// CPSC 2620 Assignment 6 - Question 3
// Briana Smith
//
// This program modifies the quicksort algorithm into an algorithm called
// quickselect which returns the kth smallest element of a user entered array.

#include<iostream>
using namespace std;

int quickSelect(int A[], int, int, int);
int partition(int A[],int, int);

int main()
{
   int userSize, userIn, k;
   char userChoice;
   do{   
      cout<<"Enter the size of array: ";
      cin>>userSize;
      int A[userSize];
      cout<<"Enter "<<userSize<<" digits (Enter after each): "<<endl;
      for(int i = 0; i<userSize; i++)
      {
	 cin>>userIn;
	 A[i] = userIn;
      }
   
      cout<<"Enter smallest element you would like from array"<<endl;
      cout<<"Program ends when k<=0"<<endl;
      cout<<"Enter k: ";
      cin>>k;
      while(k>0 && k<userSize+1)
      {
	 int kthElement = quickSelect(A,0,userSize,k);
	 cout<<"The "<<k<<" smallest element is: "<<kthElement<<endl;
	 cout<<"Enter k: ";
	 cin>>k;
      }
     
      cout<<"Enter another array? (Y/N)"<<endl;
      cin>>userChoice;
   }
   while(userChoice == 'y' || userChoice == 'Y');
      
   return 0;
}

// quickSelect
// Modified quicksort that sorts either left half or right half from initial pivot
// to output kth smallest element of array
int quickSelect(int A[], int start, int end, int k)
{
   if(end-start > 1)
   {
      int pivot = partition(A, start, end);
      // cout<<"pivot: "<<pivot<<endl;
      //cout<<"A[pivot]: "<<A[pivot]<<endl;
      if(k<=pivot)
	 quickSelect(A, start, pivot, k);

      else
	 quickSelect(A, pivot+1, end, k);
   }
      return A[k-1];
}

// partition
// Sorts array around pivot number, and returns pivot
int partition(int A[], int start, int end)
{
   int i,j;
   i = start+1;
   for(j = start+1; j<end; j++)
   {
      if(A[j] <= A[start])
	 swap(A[i++],A[j]);
   }
   swap(A[start], A[i-1]);
   return i-1;
}
