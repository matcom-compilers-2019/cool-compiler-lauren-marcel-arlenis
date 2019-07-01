class Main { main() : Int {{ new C.winky(); 0;} }; };

class A inherits IO {
	inky():Int { {out_int(1); 0;} };
};

class B inherits A {
	binky():String {{out_string("hello");"hello";}};
};

class C {
	b:B <- new B ;
	winky():Object { b@B.binky() };
};