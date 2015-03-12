#ifndef __SDA_IMPL_HPP

template<typename Alg>
SDA<Alg>::SDA(uint32_t nThr){
	stop = false;
	for(uint32_t t = 0; t < nThr; t++){
		workers.push_back(std::thread(&SDA<Alg>::worker, this));
	}
}

template<typename Alg>
SDA<Alg>::~SDA(){
	stop = true;
	queue_cond.notify_all();
	for(uint32_t i = 0; i < workers.size(); i++){
		workers[i].join();
	}
}

template<typename Alg>
SDA<Alg>::run(){

	//TODO: add jobs to the queue
}


template<typename Alg>
void SDA<Alg>::worker(){
	while(true){
		{
			std::lock_guard<std::mutex> lock(queue_mutex);
			while(!stop && jobs.empty()){
				queue_cond.wait(lock);
			}
			if (stop){
				lock.unlock();
				return;
			}

			job = jobs.front();
			jobs.pop_front();
		}//release the lock_guard

		//TODO: do the job
	}
}
#define __SDA_IMPL_HPP
#endif /* __SDA_IMPL_HPP */
