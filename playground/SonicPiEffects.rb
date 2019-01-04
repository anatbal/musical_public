#Control just the mix- mix deafult is 1. Recives values 0<=mix<=1
#No Effect
live_loop :reg do
  use_real_time
  param = sync "/osc/reg"
  mySamp = param[0]
  sample mySamp,start: param[2], finish: param[3], amp: param[4], pan: param[5]
  sleep param[6]
end

#Whammy Effect
live_loop :whammyEffect do
  use_real_time
  param = sync "/osc/whammy"
  mySamp = param[0]
  with_fx :whammy, mix: param[1] do
    sample mySamp,start: param[2], finish: param[3], amp: param[4], pan: param[5]
    sleep param[6]
  end
end

#Techno Effect
live_loop :technoEffect do
  use_real_time
  param = sync "/osc/techno"
  mySamp = param[0]
  with_fx :ixi_techno, mix: param[1] do
    sample mySamp,start: param[2], finish: param[3], amp: param[4], pan: param[5]
    sleep param[6]
  end
end

#BitCursher Effect
live_loop :bitcrusherEffect do
  use_real_time
  param = sync "/osc/bitcrusher"
  mySamp = param[0]
  with_fx :bitcrusher, mix: param[1] do
    sample mySamp,start: param[2], finish: param[3], amp: param[4], pan: param[5]
    sleep param[6]
  end
end

#BPF Effect
live_loop :bpfEffect do
  use_real_time
  param = sync "/osc/bpf"
  mySamp = param[0]
  with_fx :bpf, mix: param[1] do
    sample mySamp,start: param[2], finish: param[3], amp: param[4], pan: param[5]
    sleep param[6]
  end
end

#RHPF Effect
live_loop :rhpfEffect do
  use_real_time
  param = sync "/osc/rhpf"
  mySamp = param[0]
  with_fx :rhpf, mix: param[1] do
    sample mySamp,start: param[2], finish: param[3], amp: param[4], pan: param[5]
    sleep param[6]
  end
end