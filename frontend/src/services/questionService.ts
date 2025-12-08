export const computeBinary = (op: string, a: number, b: number): number | null => {
  try {
    switch (op) {
      case "add": return a + b;
      case "subtract": return a - b;
      case "multiply": return a * b;
      case "divide": return b !== 0 ? a / b : null;
      case "min": return Math.min(a, b);
      case "max": return Math.max(a, b);
      case "lcm": return Math.abs(a * b) / gcd(a, b); // simple LCM
      case "negate": return -a; // unary
      default: return null;
    }
  } catch {
    return null;
  }
};

const gcd = (a: number, b: number): number => {
  if (!b) return a;
  return gcd(b, a % b);
};

// ---- compute AST recursively ----
export const computeAst = (ast: string): number | null => {
  ast = ast.trim();

  // constant: const_2 or const_3_5 (float)
  const constMatch = ast.match(/^const_(-?\d+(?:_\d+)*)$/);
  if (constMatch) {
    const valStr = constMatch[1].replace("_", ".");
    return valStr.includes(".") ? parseFloat(valStr) : parseInt(valStr);
  }

  // operation: op(arg1,arg2)
  const match = ast.match(/^(\w+)\((.*)\)$/);
  if (!match) return null;

  const op = match[1];
  const argsStr = match[2];

  // Split arguments while handling nested parentheses
  const args: string[] = [];
  let depth = 0;
  let current = "";
  for (const ch of argsStr) {
    if (ch === "(") depth++;
    if (ch === ")") depth--;
    if (ch === "," && depth === 0) {
      args.push(current.trim());
      current = "";
    } else {
      current += ch;
    }
  }
  if (current) args.push(current.trim());

  if (args.length === 1) {
    const a = computeAst(args[0]);
    if (a === null) return null;
    return computeBinary(op, a, 0);
  } else if (args.length === 2) {
    const a = computeAst(args[0]);
    const b = computeAst(args[1]);
    if (a === null || b === null) return null;
    return computeBinary(op, a, b);
  } else {
    return null;
  }
};