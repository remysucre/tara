
#include <iostream>
#include "taco.h"

using namespace taco;

int main(int argc, char* argv[]) {
    Format s8({Sparse, Sparse, Sparse, Sparse, Sparse, Sparse, Sparse, Sparse});
    Tensor<double> aka_name("aka_name", {1363559, 1363560, 1644176, 1496584, 1643661, 1642761, 1643702, 1644177}, s8);

    Format s12({Sparse, Sparse, Sparse, Sparse, Sparse, Sparse, Sparse, Sparse, Sparse, Sparse, Sparse, Sparse});
    Tensor<double> aka_title("aka_title", {563713, 563702, 683273, 453990, 409, 75243, 682677, 72804, 38910, 71649, 682144, 683275}, s12);

    Format s7({Sparse, Sparse, Sparse, Sparse, Sparse, Sparse, Sparse});
    Tensor<double> cast_info("cast_info", {36244364, 4061927, 2525976, 3140340, 715572, 28821833, 25}, s7);

    Tensor<double> char_name("char_name", {2265824, 4553942, 1838472, 2, 4553762, 4446396, 4553943}, s7);

    Format s2({Sparse, Sparse});
    Tensor<double> company_type("company_type", {4, 4}, s2);
    Tensor<double> info_type("info_type", {113, 113}, s2);
    Format s5({Sparse, Sparse, Sparse, Sparse, Sparse});
    Tensor<double> movie_companies("movie_companies", {2609129, 2525745, 351779, 2, 66451}, s5);
    Tensor<double> movie_info_idx("movie_info_idx", {1686752, 1686590, 124, 146246, 2}, s5);
    Tensor<double> title("title", {2528313, 4036495, 3930377, 116, 194324, 4, 4033232, 2528187, 3974, 199930, 4012686, 4036516}, s12);

    aka_name = read("/Users/albert/tara/imdb_tns/aka_name.tns", s8, false);
    aka_title = read("/Users/albert/tara/imdb_tns/aka_title.tns", s12, false);
    cast_info = read("/Users/albert/tara/imdb_tns/cast_info.tns", s7, false);
    char_name = read("/Users/albert/tara/imdb_tns/char_name.tns", s7, false);
    company_type = read("/Users/albert/tara/imdb_tns/company_type.tns", s2, false);
    info_type = read("/Users/albert/tara/imdb_tns/info_type.tns", s2, false);
    movie_companies = read("/Users/albert/tara/imdb_tns/movie_companies.tns", s5, false);
    movie_info_idx = read("/Users/albert/tara/imdb_tns/movie_info_idx.tns", s5, false);
    title = read("/Users/albert/tara/imdb_tns/title.tns", s12, false);

    IndexVar itid, ctid, ctv1, itv1;
    Tensor<double> ct(0.0);
    ct(ctid) = company_type(ctid, ctv1);
    Tensor<double> it(0.0);
    it(itid) = info_type(itid, itv1);

    IndexVar mcid, tid, cid, note1;
    Tensor<double> mc(0.0);
    mc(tid, ctid) = movie_companies(mcid, tid, cid, ctid, note1);

    IndexVar miiid, info1, note2;
    Tensor<double> miidx(0.0);
    miidx(tid, itid) = movie_info_idx(miiid, tid, itid, info1, note2);

    IndexVar tv1, tv2, tv3, tv4, tv5, tv6, tv7, tv8, tv9, tv10, tv11;
    Tensor<double> t(0.0);
    t(tid) = title(tid, tv1, tv2, tv3, tv4, tv5, tv6, tv7, tv8, tv9, tv10, tv11);

    Tensor<double> q(0.0);
    q = ct(ctid) * it(itid) * mc(tid,ctid) * miidx(tid,itid) * t(tid);

    std::cout << q << std::endl;
}
