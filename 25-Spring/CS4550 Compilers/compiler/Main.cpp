#include <iostream>
#include "Symbol.h"
#include "Scanner.h"
#include "Token.h"
#include "Node.h"

void testScanner() {
    std::cout << "----- Scanner Test -----\n";

    const std::string inputFileName = "code.txt";
    ScannerClass scanner(inputFileName);
    TokenType tt;
    try {
        do {
            TokenClass tc = scanner.GetNextToken();
            std::cout << "Line " << scanner.GetLineNumber() << ": " << tc << std::endl;
            tt = tc.GetTokenType();
        } while (tt != ENDFILE_TOKEN);
    }
    catch (const std::exception &e) {
        std::cerr << "Error (Scanner): " << e.what() << std::endl;
        std::exit(1);
    }
}

void testSymbolTable() {
    std::cout << "\n----- Symbol Table Test -----\n";

    SymbolTableClass symbolTable;
    symbolTable.AddEntry("x");
    symbolTable.AddEntry("y");

    std::cout << "Symbol count: " << symbolTable.GetCount() << std::endl;  // Expected: 2
    std::cout << "Exists 'x'? " << (symbolTable.Exists("x") ? "true" : "false") << std::endl;  // Expected: true
    std::cout << "Exists 'z'? " << (symbolTable.Exists("z") ? "true" : "false") << std::endl;  // Expected: false
    std::cout << "Index of 'x': " << symbolTable.GetIndex("x") << std::endl;   // Expected: 0
    std::cout << "Index of 'y': " << symbolTable.GetIndex("y") << std::endl;   // Expected: 1

    std::cout << "Value of 'x': " << symbolTable.GetValue("x") << std::endl;  // Expected: 0
    symbolTable.SetValue("x", 42);
    std::cout << "New value of 'x': " << symbolTable.GetValue("x") << std::endl;  // Expected: 42

    // Uncomment these to test error handling:
    // symbolTable.AddEntry("x");
    // symbolTable.GetValue("z");
    // symbolTable.SetValue("z", 10);
}

void testNodes() {
    std::cout << "\n----- Node (Parse Tree) Test -----\n";

    // 1) Create a small expression tree: 10 + 20
    ExpressionNode* plusExpr = new PlusNode(
        new IntegerNode(10),
        new IntegerNode(20)
    );
    // Test Evaluate (should print 30)
    std::cout << "Evaluate(10 + 20) = " << plusExpr->Evaluate() << std::endl;

    // 2) Create a tiny snippet of statements:
    //    int x;        (DeclarationStatementNode)
    //    x = 10 + 20;  (AssignmentStatementNode)
    //    cout << x;    (CoutStatementNode)

    // Declaration: int x;
    StatementNode* declStmt = new DeclarationStatementNode(
        new IdentifierNode("x")
    );

    // Assignment: x = (plusExpr) or build a fresh expression:
    ExpressionNode* plusExpr2 = new PlusNode(
        new IntegerNode(10),
        new IntegerNode(20)
    );
    StatementNode* assignStmt = new AssignmentStatementNode(
        new IdentifierNode("x"),
        plusExpr2
    );

    // cout << x;
    StatementNode* coutStmt = new CoutStatementNode(
        new IdentifierNode("x")
    );

    // 3) Put these statements into a StatementGroupNode
    StatementGroupNode* stmtGroup = new StatementGroupNode();
    stmtGroup->AddStatement(declStmt);
    stmtGroup->AddStatement(assignStmt);
    stmtGroup->AddStatement(coutStmt);

    // 4) Wrap the StatementGroupNode in a BlockNode
    BlockNode* blockNode = new BlockNode(stmtGroup);

    // 5) Create a ProgramNode that holds this BlockNode
    ProgramNode* programNode = new ProgramNode(blockNode);

    // 6) Finally, create a StartNode that holds the ProgramNode
    StartNode* startNode = new StartNode(programNode);

    // 7) Clean up.
    delete plusExpr;  // This is the stand-alone expression.
    delete startNode; // Recursively deletes all child nodes.
}

int main() {
    //testScanner();      // 1) Test the scanner
    //testSymbolTable();  // 2) Test the symbol table
    testNodes();        // 3) Test parse-tree nodes
    return 0;
}
