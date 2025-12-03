#!/usr/bin/bash
sed -e 's/TALC\.globals//g; s/globals//g; s/\.//g; s/TLAC//g; s/globals\.//g; 1,8d; s/(\,/(/g' problem3-program.py > problem3-program-simplified.py
sed -e 's/TALC\.globals//g; s/globals//g; s/\.//g; s/TLAC//g; s/globals\.//g; 1,8d' problem4-program.py > problem4-program-simplified.py
sed -e 's/,//g; s/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' problem5-program.py > problem5-program-simplified.py
sed -e 's/,//g; s/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' problem6-program.py > problem6-program-simplified.py
sed -e 's/,//g; s/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' problem7-program.py > problem7-program-simplified.py
sed -e 's/,//g; s/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' problem8-program.py > problem8-program-simplified.py
#docs
sed -e 's/,//g; s/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' docs_functionsEN.py > docs_functionsEN-simplified.py
sed -e 's/,//g; s/TALC\.globals//g; s/globals//g; s/\.//g;s/TLAC//g; s/globals\.//g; 1,8d' docs_very_basic_program.py > docs_very_basic_program-simplified.py
sed -e 's/TLAC\.//g; s/TLAC\.globals/,/g; s/globals//g; s/ ,//g; s/\.turtle\./turtle/g; s/^ //g; 1,8d' docs_user_input_example.py > docs_user_input_example-simplified.py
sed -e 's/TLAC\.//g; s/TLAC\.globals\./,/g; s/ globals,//g; s/ ,//g; s/globals\.//g; s/globals,//g; s/\.turtle\./turtle/g; 1,9d' docs_loops_countdown.py > docs_loops_countdown-simplified.py
sed -e 's/TLAC\.//g; s/TLAC\.globals\./,/g; s/ globals,//g; s/ ,//g; s/globals\.//g; s/globals,//g; s/\.turtle\./turtle/g; 1,9d' docs_loops_do_while.py > docs_loops_do_while-simplified.py
sed -e 's/TLAC\.//g; s/TLAC\.globals\./,/g; s/ globals,//g; s/ ,//g; s/globals\.//g; s/globals,//g; s/\.turtle\./turtle/g; 1,9d' docs_loops_forloop.py > docs_loops_forloop-simplified.py 
sed -e 's/TLAC\.//g; s/TLAC\.globals\./,/g; s/ globals,//g; s/ ,//g; s/globals\.//g; s/globals,//g; s/\.turtle\./turtle/g; 1,9d' docs_loops_foreachLoop.py > docs_loops_foreachLoop-simplified.py 
sed -e 's/TLAC\.//g; s/TLAC\.globals\./,/g; s/ globals,//g; s/ ,//g; s/globals\.//g; s/globals,//g; s/\.turtle\./turtle/g; 1,9d' docs_loops_nested_forloops.py > docs_loops_nested_forloops-simplified.py
sed -e 's/TLAC\.//g; s/TLAC\.globals\./,/g; s/ globals,//g; s/ ,//g; s/globals\.//g; s/globals,//g; s/\.turtle\./turtle/g; 1,9d' docs_operations_on_lists.py > docs_operations_on_lists-simplified.py
sed -e 's/TLAC\.//g; s/TLAC\.globals\./,/g; s/ globals,//g; s/ ,//g; s/globals\.//g; s/globals,//g; s/\.turtle\./turtle/g; 1,9d' docs_loops_multiple_forloops.py > docs_loops_multiple_forloops-simplified.py
#algorythms
sed -e 's/TLAC\.//g; s/TLAC\.globals\./,/g; s/ globals,//g; s/ ,//g; s/globals\.//g; s/globals,//g; s/\.turtle\./turtle/g; 1,9d' algorythm-insertionSortNew.py  > algorythm-insertionSortNew-simplified.py
sed -e 's/TLAC\.globals)/)/g;s/TLAC.globals,//g;s/TLAC\.//g;s/TLAC\.globals\./,/g;s/ globals,//g;s/ ,//g;s/globals\.//g;s/globals,//g;s/\.turtle\./turtle/g;1,9d' algorithm-mazeTest.py > mazeTest-simplified.py
sed -e 's/TLAC\.globals)/)/g;s/TLAC.globals,//g;s/TLAC\.//g;s/TLAC\.globals\./,/g;s/ globals,//g;s/ ,//g;s/globals\.//g;s/globals,//g;s/\.turtle\./turtle/g;1,9d' algorithm-insertion-sort-pyramids.py > algorithm-insertion-sort-pyramids-simplified.py