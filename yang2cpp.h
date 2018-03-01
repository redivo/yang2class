/**************************************************************************************************/
/**
 * \file
 * \brief Basics classes used in YANG generator
 */
/**************************************************************************************************/

#ifndef __YANG2CPP_H__
#define __YANG2CPP_H__

#include <string>
#include <map>
#include <stdint.h>

/**************************************************************************************************/

namespace CppYangModel {

class BasicNode {
   public:
    BasicNode(std::string path) : path_(path) {}

   private:
    std::string path_;
};

template <class T>
class Leaf : public BasicNode {
   public:
    Leaf(std::string path) : BasicNode(path) {}

    void setValue(const T& value) {
        value_ = value;
    }

    T getValue() {
        return value_;
    }

   private:
    T value_;
};

} /* namespace CppYangModel */

#endif /* __YANG2CPP_H__ */
