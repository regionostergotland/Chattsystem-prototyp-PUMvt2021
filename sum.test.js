const func = require('./sum');

sum = func[0]

test('adds 1 + 2 to equal 3', () => {
	expect(sum(1, 2)).toBe(3);
});

foo = func[1]

test('adds 1 + 1 to equal 2', () => {
	expect(foo(1)).toBe(2);
});
