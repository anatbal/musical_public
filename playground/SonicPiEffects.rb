live_loop :effect do
  use_real_time
  param = sync "/osc/effect"
  mySamp = param[0]
  with_fx :whammy, mix: param[6] do
    with_fx :ixi_techno, mix: param[7] do
      with_fx :bitcrusher, mix: param[8] do
        with_fx :bpf, mix: param[9] do
          with_fx :rhpf, mix: param[10] do
            sample mySamp,start: param[1], finish: param[2], amp: param[4], pan: param[5]
            sleep param[3]
          end
        end
      end
    end
  end
end