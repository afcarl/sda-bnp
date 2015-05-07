#ifndef __TRACE_HPP
#include<string>
#include<fstream>
#include<sstream>
#include<iostream>

template<class Dist>
class Trace{
	public:
		std::vector<double> times, objs, testlls;
		std::vector<Dist> dists;
		void clear(){
			times.clear();
			objs.clear();
			testlls.clear();
			dists.clear();
		}
		void save(std::string name){
			std::ofstream out_trc(name+"-trace.log", std::ios_base::trunc);
			if (testlls.size() == times.size()){
				for (uint32_t i = 0; i < times.size(); i++){
					out_trc << times[i] << " " << objs[i] << " " << testlls[i] << std::endl;
				}
			} else {
				for (uint32_t i = 0; i < times.size(); i++){
					out_trc << times[i] << " " << objs[i] << std::endl;
				}
			}
			out_trc.close();
		}
};

template<class Dist>
class MultiTrace{
	public:
		std::vector<double> globaltimes, globaltestlls;
		std::vector<Dist> globaldists;
		std::vector<uint32_t> globalclusters, globalmatchings;
		std::vector< std::vector<double> > localtimes, localobjs, localtestlls;
		std::vector< std::vector<Dist> > localdists;
		std::vector<double> localstarttimes, localmergetimes;
		void clear(){
			globaltimes.clear();
			globaltestlls.clear();
			globalclusters.clear();
			globalmatchings.clear();
			globaldists.clear();
			localmergetimes.clear();
			localtimes.clear();
			localobjs.clear();
			localtestlls.clear();
			localstarttimes.clear();
			localdists.clear();
		}
		void save(std::string name){
			//for a multitrace, the only thing to output is testll
			//so if this isn't the right size, forget it
			if (globaltimes.size() != globaltestlls.size()){
				std::cout << "Error -- globaltimes.size() != globaltestlls.size()!" << std::endl;
				return;
			}
			std::ofstream out_trc(name+"-globaltrace.log", std::ios_base::trunc);
			for (uint32_t i = 0; i < globaltimes.size(); i++){
				out_trc << globaltimes[i] << " " << globaltestlls[i] << " " << globalclusters[i] << " " << globalmatchings[i] << std::endl;
			}
			out_trc.close();

			std::ofstream out_tms(name + "-localtimes.log", std::ios_base::trunc);
			for (uint32_t i = 0; i < localstarttimes.size(); i++){
				out_tms << localstarttimes[i] << " " << localmergetimes[i] << std::endl;
			}
			out_tms.close();

			for (uint32_t i = 0; i < localtimes.size(); i++){
				std::ostringstream oss;
				oss << name << "-localtrace-" << i << ".log";
				std::ofstream out_ltrc(oss.str().c_str(), std::ios_base::trunc);
				for (uint32_t j = 0; j < localtimes[i].size(); j++){
					out_ltrc << localtimes[i][j] << " " << localobjs[i][j];
					if (j < localtestlls[i].size()){
						out_ltrc << " " << localtestlls[i][j] << std::endl;
					} else {
						out_ltrc << std::endl;
					}
				}
				out_ltrc.close();
			}
		}
};
#define __TRACE_HPP
#endif /* __TRACE_HPP */
