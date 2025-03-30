#include <iostream>
#include "Symbol.h"
#include "Scanner.h"
#include "Token.h"
#include "Node.h"
#include "Parser.h"

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

    // Create a SymbolTable for IdentifierNodes
    SymbolTableClass symbolTable;
    symbolTable.AddEntry("x");
    symbolTable.AddEntry("y");
    symbolTable.AddEntry("z");

    // Test arithmetic operators

    // 10 + 20
    ExpressionNode* plusExpr = new PlusNode(
        new IntegerNode(10),
        new IntegerNode(20)
    );
    std::cout << "Evaluate(10 + 20) = " << plusExpr->Evaluate() << std::endl;
    delete plusExpr;

    // 6 * 7
    ExpressionNode* timesExpr = new TimesNode(
        new IntegerNode(6),
        new IntegerNode(7)
    );
    std::cout << "Evaluate(6 * 7) = " << timesExpr->Evaluate() << std::endl;
    delete timesExpr;

    // 12 - 5
    ExpressionNode* minusExpr = new MinusNode(
        new IntegerNode(12),
        new IntegerNode(5)
    );
    std::cout << "Evaluate(12 - 5) = " << minusExpr->Evaluate() << std::endl;
    delete minusExpr;

    // 48 / 6
    ExpressionNode* divideExpr = new DivideNode(
        new IntegerNode(48),
        new IntegerNode(6)
    );
    std::cout << "Evaluate(48 / 6) = " << divideExpr->Evaluate() << std::endl;
    delete divideExpr;

    // Test some relational operators
    // 3 < 5
    ExpressionNode* lessExpr = new LessNode(
        new IntegerNode(3),
        new IntegerNode(5)
    );
    std::cout << "Evaluate(3 < 5) = " << lessExpr->Evaluate() << std::endl; // expected 1
    delete lessExpr;

    // 10 == 10
    ExpressionNode* equalExpr = new EqualNode(
        new IntegerNode(10),
        new IntegerNode(10)
    );
    std::cout << "Evaluate(10 == 10) = " << equalExpr->Evaluate() << std::endl; // expected 1
    delete equalExpr;

    //    int x;
    //    int y;
    //    int z;
    //    x = 10 + 20;
    //    y = (x - 10) / 2;
    //    z = (x < y);
    //    cout << z;

    // Declarations
    StatementNode* declX = new DeclarationStatementNode(
        new IdentifierNode("x", &symbolTable)
    );
    StatementNode* declY = new DeclarationStatementNode(
        new IdentifierNode("y", &symbolTable)
    );
    StatementNode* declZ = new DeclarationStatementNode(
        new IdentifierNode("z", &symbolTable)
    );

    // x = 10 + 20
    ExpressionNode* assignXExpr = new PlusNode(
        new IntegerNode(10),
        new IntegerNode(20)
    );
    StatementNode* assignX = new AssignmentStatementNode(
        new IdentifierNode("x", &symbolTable),
        assignXExpr
    );

    // y = (x - 10) / 2
    ExpressionNode* minusX10 = new MinusNode(
        new IdentifierNode("x", &symbolTable),
        new IntegerNode(10)
    );
    ExpressionNode* divideExpr2 = new DivideNode(
        minusX10,
        new IntegerNode(2)
    );
    StatementNode* assignY = new AssignmentStatementNode(
        new IdentifierNode("y", &symbolTable),
        divideExpr2
    );

    // z = (x < y)
    ExpressionNode* lessXY = new LessNode(
        new IdentifierNode("x", &symbolTable),
        new IdentifierNode("y", &symbolTable)
    );
    StatementNode* assignZ = new AssignmentStatementNode(
        new IdentifierNode("z", &symbolTable),
        lessXY
    );

    // cout << z
    StatementNode* coutZ = new CoutStatementNode(
        new IdentifierNode("z", &symbolTable)
    );

    // Put these statements into a StatementGroupNode
    StatementGroupNode* stmtGroup = new StatementGroupNode();
    stmtGroup->AddStatement(declX);
    stmtGroup->AddStatement(declY);
    stmtGroup->AddStatement(declZ);
    stmtGroup->AddStatement(assignX);
    stmtGroup->AddStatement(assignY);
    stmtGroup->AddStatement(assignZ);
    stmtGroup->AddStatement(coutZ);

    // Wrap the StatementGroupNode in a BlockNode
    BlockNode* blockNode = new BlockNode(stmtGroup);

    // Create a ProgramNode that holds this BlockNode
    ProgramNode* programNode = new ProgramNode(blockNode);

    // Create a StartNode that holds the ProgramNode
    StartNode* startNode = new StartNode(programNode);

    // Delete the entire tree (recursively frees all children)
    delete startNode;

    std::cout << "\nFinished Node (Parse Tree) Test.\n";
}

void testParserNoOutput() {
    std::cout << "\n----- Parser Test -----\n";

    // Setup a scanner to read from "code.txt"
    //    (Adjust filename as needed.)
    const std::string inputFileName = "code.txt";
    ScannerClass scanner(inputFileName);

    // Create a symbol table
    SymbolTableClass symbolTable;

    // Create a Parser with the scanner and symbol table
    ParserClass parser(&scanner, &symbolTable);

    // Call parser.Start()
    //    If the tokens in "code.txt" follow the grammar, it should succeed silently.
    //    If there's an error, parser.Start() will print a message and exit(1).
    parser.Start();

    // If we reach here, no errors were found.
    std::cout << "Parser recognized the input as valid." << std::endl;
}

void testParserWithOutput() {
    std::cout << "\n----- Parser With Output Test -----\n";

    // Create a scanner to read your source file "code.txt"
    const std::string inputFileName = "code.txt";
    ScannerClass scanner(inputFileName);

    // Create a symbol table
    SymbolTableClass symbolTable;

    // Create a parser that returns parse-tree nodes
    ParserClass parser(&scanner, &symbolTable);

    // The parser's Start() now returns a StartNode*
    // That pointer is your entire parse tree's root, if no error occurs.
    StartNode* root = parser.Start();

    // If we got here, the parse was successful.
    std::cout << "Parser returned a StartNode. The input is valid!\n";

    // Recusrively delete the tree:
    delete root;
    std::cout << "Parse tree deleted.\n";
}

void testInterpreter() {
    std::cout << "\n----- Interpreter Test -----\n";

    // same as parser test
    const std::string inputFileName = "code.txt";
    ScannerClass scanner(inputFileName);
    SymbolTableClass symbolTable;
    ParserClass parser(&scanner, &symbolTable);
    StartNode* root = parser.Start();
    std::cout << "Parser built a StartNode. The input is valid!\n";

    // add this
    std::cout << "Interpreting the parse tree...\n";
    root->Interpret();

    delete root;
    std::cout << "Finished interpretation and parse tree cleanup.\n";
}


int main() {
    //testScanner();
    //testSymbolTable();
    //testNodes();
    //testParserNoOutput();
    //testParserWithOutput();
    testInterpreter();

    return 0;
}
