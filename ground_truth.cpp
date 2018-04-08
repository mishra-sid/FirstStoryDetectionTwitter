#include <bits/stdc++.h>

using namespace std;

template<typename Out>
void split(const std::string &s, char delim, Out result) {
  std::stringstream ss(s);
  std::string item;
  while (std::getline(ss, item, delim)) {
    *(result++) = item;
  }
}

std::vector<std::string> split(const std::string &s, char delim) {
  std::vector<std::string> elems;
  split(s, delim, std::back_inserter(elems));
  return elems;
}

int main() {
   vector<set<string>> stories;
   int nstories = 8203;
   for(int i = 1; i <= nstories; i++) {
      ifstream file("stories/" + to_string(i));
      stringstream buffer;
      buffer << file.rdbuf();
      string curr = buffer.str();
      set<string> cs;
      for(string & s : split(curr, ' ')) {
        string ns = "";
        for(char c : s) {
          if(isalnum(c)) 
            ns += c; 
        }
        cs.insert(ns);
      }
      stories.push_back(cs);
   }
   vector<int> truthcount(10, 0); 
   for(int i = 0; i < nstories; i++) {
     cout << " i = " << i << "\n";
     for(int j = 0; j < i; j++) {
       set<string> a = stories[i], b = stories[j];
       set<string> intersection_story;
       set<string> union_story;
       set_intersection(a.begin(), a.end(), b.begin(), b.end(), inserter(intersection_story, intersection_story.begin()));
       set_union(a.begin(), a.end(), b.begin(), b.end(), inserter(union_story, union_story.begin()));
       double score = double(intersection_story.size())/union_story.size();
       int bucket = int(score / 0.1);
       truthcount[bucket] += 1;
    }
   }
   for(int i = 0; i < 10; i++) {
      cout << "The number of pairs with similarity score in range " << 0.1 * i << " " << 0.1 * (i + 1) << "are : " << truthcount[i] << "\n"; 
   }
  return 0;
}
