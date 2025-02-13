#include "Symbol.h"
#include <iostream>
#include <cstdlib>

// Check if the symbol exists
bool SymbolTableClass::Exists(const std::string & s) const
{
    for (size_t i = 0; i < mSymbols.size(); i++)
    {
        if (mSymbols[i].mLabel == s)
            return true;
    }
    return false;
}

// Add a new symbol to the table
void SymbolTableClass::AddEntry(const std::string & s)
{
    if (Exists(s))
    {
        std::cerr << "Error: Symbol \"" << s << "\" already exists in the symbol table.\n";
        std::exit(1);
    }
    Variable var;
    var.mLabel = s;
    var.mValue = 0;  // Default initial value
    mSymbols.push_back(var);
}

// Return the value of the given symbol
int SymbolTableClass::GetValue(const std::string & s) const
{
    for (size_t i = 0; i < mSymbols.size(); i++)
    {
        if (mSymbols[i].mLabel == s)
            return mSymbols[i].mValue;
    }
    std::cerr << "Error: Symbol \"" << s << "\" does not exist in the symbol table.\n";
    std::exit(1);
    return 0; // Should be unreachable
}

// Set the value of the given symbol
void SymbolTableClass::SetValue(const std::string & s, int v)
{
    for (size_t i = 0; i < mSymbols.size(); i++)
    {
        if (mSymbols[i].mLabel == s)
        {
            mSymbols[i].mValue = v;
            return;
        }
    }
    std::cerr << "Error: Symbol \"" << s << "\" does not exist in the symbol table.\n";
    std::exit(1);
}

// Return the index of the symbol in the table, return -1 if not found
int SymbolTableClass::GetIndex(const std::string & s) const
{
    for (size_t i = 0; i < mSymbols.size(); i++)
    {
        if (mSymbols[i].mLabel == s)
            return static_cast<int>(i);
    }
    return -1;
}

// Return the total number of symbols
size_t SymbolTableClass::GetCount() const
{
    return mSymbols.size();
}
