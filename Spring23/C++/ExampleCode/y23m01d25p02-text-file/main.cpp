#include <fstream>
#include <string>
#include <vector>

int main() {
  std::vector<std::string> words = {"the", "quick", "brown", "fox"};

  std::ofstream word_file("words.txt"); // creates an output stream, associated with the file words.txt

  unsigned int i;
  for(i = 0; i < words.size(); i++) {
    word_file << words[i] << " ";
  }
  int x = 13;
  int y = 7;
  word_file << x << " " << y;
  word_file << std::endl;
  
  word_file.close();
  return 0;
}
