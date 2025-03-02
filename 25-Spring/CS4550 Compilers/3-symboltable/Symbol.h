#pragma once
#include <string>
#include <vector>

class SymbolTableClass {
private:
    struct Variable {
        std::string mLabel; // variable name
        int mValue;
    };
    std::vector<Variable> mSymbols;

public:
    bool Exists(const std::string & s) const;
    void AddEntry(const std::string & s);
    int GetValue(const std::string & s) const;
    void SetValue(const std::string & s, int v);
    int GetIndex(const std::string & s) const;
    size_t GetCount() const;
};
