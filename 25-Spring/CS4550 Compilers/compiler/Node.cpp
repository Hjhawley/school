#include "Node.h"
#include "Symbol.h"
#include "Debug.h"  // For the MSG macro
#include <cstdlib>

// Base Class Node
Node::~Node() {
    MSG("~Node() called");
}

// StartNode
StartNode::StartNode(ProgramNode* program)
    : mProgram(program) {
}

StartNode::~StartNode() {
    MSG("~StartNode() called");
    delete mProgram;
}

ProgramNode* StartNode::GetProgram() const {
    return mProgram;
}

// ProgramNode
ProgramNode::ProgramNode(BlockNode* block)
    : mBlock(block) {
}

ProgramNode::~ProgramNode() {
    MSG("~ProgramNode() called");
    delete mBlock;
}

BlockNode* ProgramNode::GetBlock() const {
    return mBlock;
}

// BlockNode
BlockNode::BlockNode(StatementGroupNode* statementGroup)
    : mStatementGroup(statementGroup) {
}

BlockNode::~BlockNode() {
    MSG("~BlockNode() called");
    delete mStatementGroup;
}

StatementGroupNode* BlockNode::GetStatementGroup() const {
    return mStatementGroup;
}

// StatementGroupNode
StatementGroupNode::StatementGroupNode() {
}

StatementGroupNode::~StatementGroupNode() {
    MSG("~StatementGroupNode() called");
    for (StatementNode* stmt : mStatements) {
        delete stmt;
    }
}

void StatementGroupNode::AddStatement(StatementNode* stmt) {
    mStatements.push_back(stmt);
}

const std::vector<StatementNode*>& StatementGroupNode::GetStatements() const {
    return mStatements;
}

// StatementNode
StatementNode::~StatementNode() {
    MSG("~StatementNode() called");
}

// DeclarationStatementNode
DeclarationStatementNode::DeclarationStatementNode(IdentifierNode* identifier)
    : mIdentifier(identifier) {
}

DeclarationStatementNode::~DeclarationStatementNode() {
    MSG("~DeclarationStatementNode() called");
    delete mIdentifier;
}

IdentifierNode* DeclarationStatementNode::GetIdentifier() const {
    return mIdentifier;
}

// AssignmentStatementNode
AssignmentStatementNode::AssignmentStatementNode(IdentifierNode* identifier, ExpressionNode* expression)
    : mIdentifier(identifier), mExpression(expression) {
}

AssignmentStatementNode::~AssignmentStatementNode() {
    MSG("~AssignmentStatementNode() called");
    delete mIdentifier;
    delete mExpression;
}

IdentifierNode* AssignmentStatementNode::GetIdentifier() const {
    return mIdentifier;
}

ExpressionNode* AssignmentStatementNode::GetExpression() const {
    return mExpression;
}

// CoutStatementNode
CoutStatementNode::CoutStatementNode(ExpressionNode* expression)
    : mExpression(expression) {
}

CoutStatementNode::~CoutStatementNode() {
    MSG("~CoutStatementNode() called");
    delete mExpression;
}

ExpressionNode* CoutStatementNode::GetExpression() const {
    return mExpression;
}

// ExpressionNode
ExpressionNode::~ExpressionNode() {
    MSG("~ExpressionNode() called");
}

// IntegerNode
IntegerNode::IntegerNode(int value)
    : mValue(value) {
}

IntegerNode::~IntegerNode() {
    MSG("~IntegerNode(" << mValue << ") called");
}

int IntegerNode::Evaluate() const {
    return mValue;
}

// IdentifierNode
IdentifierNode::IdentifierNode(const std::string& label, SymbolTableClass* symbolTable)
    : mLabel(label), mSymbolTable(symbolTable) {
}

IdentifierNode::~IdentifierNode() {
    MSG("~IdentifierNode(" << mLabel << ") called");
}

int IdentifierNode::Evaluate() const {
    return mSymbolTable->GetValue(mLabel);
}

void IdentifierNode::DeclareVariable() {
    mSymbolTable->AddEntry(mLabel);
}

void IdentifierNode::SetValue(int v) {
    mSymbolTable->SetValue(mLabel, v);
}

int IdentifierNode::GetIndex() const {
    return mSymbolTable->GetIndex(mLabel);
}

// BinaryOperatorNode
BinaryOperatorNode::BinaryOperatorNode(ExpressionNode* left, ExpressionNode* right)
    : mLeft(left), mRight(right) {
}

BinaryOperatorNode::~BinaryOperatorNode() {
    MSG("~BinaryOperatorNode() called");
    delete mLeft;
    delete mRight;
}

// PlusNode
PlusNode::PlusNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

PlusNode::~PlusNode() {
    MSG("~PlusNode() called");
}

int PlusNode::Evaluate() const {
    return mLeft->Evaluate() + mRight->Evaluate();
}

// MinusNode
MinusNode::MinusNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

MinusNode::~MinusNode() {
    MSG("~MinusNode() called");
}

int MinusNode::Evaluate() const {
    return mLeft->Evaluate() - mRight->Evaluate();
}

// TimesNode
TimesNode::TimesNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

TimesNode::~TimesNode() {
    MSG("~TimesNode() called");
}

int TimesNode::Evaluate() const {
    return mLeft->Evaluate() * mRight->Evaluate();
}

// DivideNode
DivideNode::DivideNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

DivideNode::~DivideNode() {
    MSG("~DivideNode() called");
}

int DivideNode::Evaluate() const {
    int rightVal = mRight->Evaluate();
    return mLeft->Evaluate() / rightVal;
}

// LessNode
LessNode::LessNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

LessNode::~LessNode() {
    MSG("~LessNode() called");
}

int LessNode::Evaluate() const {
    return (mLeft->Evaluate() < mRight->Evaluate()) ? 1 : 0;
}

// LessEqualNode
LessEqualNode::LessEqualNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

LessEqualNode::~LessEqualNode() {
    MSG("~LessEqualNode() called");
}

int LessEqualNode::Evaluate() const {
    return (mLeft->Evaluate() <= mRight->Evaluate()) ? 1 : 0;
}

// GreaterNode
GreaterNode::GreaterNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

GreaterNode::~GreaterNode() {
    MSG("~GreaterNode() called");
}

int GreaterNode::Evaluate() const {
    return (mLeft->Evaluate() > mRight->Evaluate()) ? 1 : 0;
}

// GreaterEqualNode
GreaterEqualNode::GreaterEqualNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

GreaterEqualNode::~GreaterEqualNode() {
    MSG("~GreaterEqualNode() called");
}

int GreaterEqualNode::Evaluate() const {
    return (mLeft->Evaluate() >= mRight->Evaluate()) ? 1 : 0;
}

// EqualNode
EqualNode::EqualNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

EqualNode::~EqualNode() {
    MSG("~EqualNode() called");
}

int EqualNode::Evaluate() const {
    return (mLeft->Evaluate() == mRight->Evaluate()) ? 1 : 0;
}

// NotEqualNode
NotEqualNode::NotEqualNode(ExpressionNode* left, ExpressionNode* right)
    : BinaryOperatorNode(left, right) {
}

NotEqualNode::~NotEqualNode() {
    MSG("~NotEqualNode() called");
}

int NotEqualNode::Evaluate() const {
    return (mLeft->Evaluate() != mRight->Evaluate()) ? 1 : 0;
