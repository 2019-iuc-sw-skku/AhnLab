task: main.o process.o module.o autostart.o service.o reserved.o
	g++ -o task main.o process.o module.o autostart.o service.o reserved.o
main.o: main.cpp
	g++ -c -o main.o main.cpp
process.o: process.cpp
	g++ -c -o process.o process.cpp
module.o: module.cpp
	g++ -c -o module.o module.cpp
autostart.o: autostart.cpp
	g++ -c -o autostart.o autostart.cpp
service.o: service.cpp
	g++ -c -o service.o service.cpp
reserved.o: reserved.cpp
	g++ -c -o reserved.o reserved.cpp
all: task
clean:
	rm -f *.o
	rm -f task
