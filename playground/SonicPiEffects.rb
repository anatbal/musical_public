live_loop :effect do
  use_real_time
  param = sync "/osc/effect"
  with_fx :eq, high: param[7], low: param[8] do
    mySamp = param[0]
    sample mySamp,start: param[1], finish: param[2], amp: param[4], pan: param[5], release: param[6]
    sleep param[3]
  end
end
