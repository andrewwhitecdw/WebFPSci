const fs = require('fs');
const assert = require('assert');

const source = fs.readFileSync(__dirname + '/../js/fps.js', 'utf8');

// Count declarations of randSign (function declaration or var assignment)
const functionDecl = (source.match(/function\s+randSign\s*\(/g) || []).length;
const varAssign = (source.match(/var\s+randSign\s*=/g) || []).length;
const total = functionDecl + varAssign;

assert.strictEqual(total, 1, `Expected exactly one randSign definition, found ${total}`);
