#ifndef __TIMER_HPP
#include <chrono>

class Timer{
	public:
		Timer();
		void start();
		double stop();
		double get();
	private:
		std::chrono::time_point<std::chrono::high_resolution_clock> t0;
		std::chrono::duration<double> elapsed;
};


Timer::Timer(){
	this->elapsed = std::chrono::duration<double>(0);
}

void Timer::start(){
	t0 = std::chrono::high_resolution_clock::now();
}

double Timer::stop(){
	this->elapsed += (std::chrono::high_resolution_clock::now() - this->t0);
	return std::chrono::duration_cast<std::chrono::duration<double> >(this->elapsed).count();
}

double Timer::get(){
	return std::chrono::duration_cast<std::chrono::duration<double> >(this->elapsed + (std::chrono::high_resolution_clock::now() - this->t0)).count();
}

#define __TIMER_HPP
#endif /* __TIMER_HPP */
