// BST.cc
// Briana Smith
// April 4, 2017
// Assignment 6
// This is the binary search tree implementation file.

#include "BST.h"
#include<iostream> // for testing purposes

//constructor
BST::BST()
{
   root=nullptr;
}

//destructor
BST::~BST()
{
   destroy(root);
}

// Destroy
// Helper function to deallocate entire BST
void BST::destroy(Node* &root)
{
   if(root)
   {
      destroy(root->lPtr);
      destroy(root->rPtr);
      delete root;
      root = nullptr;
   }
}

// Overloaded subscript operator
// Operator [] takes string key and returns vector<string>
// with matching key
vector<string>& BST::operator[](const string& key)
{
   if(!root)
   {
      root = new Node(key, nullptr, nullptr);
      return root->value;
   }
   
   Node* tempPtr = find(root,key);
   
   if(tempPtr == nullptr)
      return insert(root,key)->value;
   
   else
      return tempPtr->value;
}

// Find
// Looks for node in tree with matching key to string.
// If match found returns pointer to that node, if no
// match returns nullptr.
BST::Node* BST::find(Node* n, const string& str)
{  
   if(n->key == str)
      return n;

    else if(n->lPtr == nullptr || n->rPtr == nullptr)
      return nullptr;
   
   else if(n->key > str)
      return find(n->lPtr, str);
   
   else //if(n->key < str)
      return find(n->rPtr,str); 
}

// Insert
// If no node exists with matching key inserts node,
// if key is same as string returns node.
BST::Node* BST::insert(Node*& n, const string& str)
{
   if(!n)
   {
      n = new Node(str, nullptr, nullptr);
      return n;
   }

   else if(n->key == str)
      return n;

   else if(n->key > str) //lower alphabetical on left
      return insert(n->lPtr, str);
   
   else //if(n->key < str) //higher alphabetical on right
   return insert(n->rPtr, str);
}

// Public Traverse
// available to user to traverse tree
void BST::traverse(void(*f)(const string& key, vector<string>& value))
{
   traverse(root,(f));
}

// Private Traverse- takes root of subtree to traverse
void BST::traverse(Node* root, void(*f)(const string& key, vector<string>& value))
{
   //traverse left, root, right
   if(root)
   {
      traverse(root->lPtr,f);
      f(root->key,root->value);
      traverse(root->rPtr, f);
   }
}
