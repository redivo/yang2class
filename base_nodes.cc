/**************************************************************************************************/

#include "base_nodes.h"

namespace Yang2Cpp {

/**************************************************************************************************/
/* BaseNode                                                                                       */
/**************************************************************************************************/

BaseNode::BaseNode(std::string path) : path_(path)
{
}

/**************************************************************************************************/

const std::string& BaseNode::GetPath() const
{
    return path_;
}

bool BaseNode::IsPresent() const
{
    return is_present_;
}

void BaseNode::SetPresence(bool presence)
{
    is_present_ = presence;
}

/**************************************************************************************************/
/* Leafs                                                                                           */
/**************************************************************************************************/

LeafBoolean::LeafBoolean(std::string path) : BaseNode(path) {
}

bool LeafBoolean::GetValue() const
{
    return value_;
}

void LeafBoolean::SetValue(bool value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

LeafDecimal64::LeafDecimal64(std::string path) : BaseNode(path)
{
}

int64_t LeafDecimal64::GetValue() const
{
    return value_;
}

void LeafDecimal64::SetValue(int64_t value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

LeafEmpty::LeafEmpty(std::string path) : BaseNode(path)
{
}

/**************************************************************************************************/

LeafInt8::LeafInt8(std::string path) : BaseNode(path)
{
}

int8_t LeafInt8::GetValue() const
{
    return value_;
}

void LeafInt8::SetValue(int8_t value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

LeafInt16::LeafInt16(std::string path) : BaseNode(path)
{
}

int16_t LeafInt16::GetValue() const
{
    return value_;
}

void LeafInt16::SetValue(int16_t value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

LeafInt32::LeafInt32(std::string path) : BaseNode(path)
{
}

int32_t LeafInt32::GetValue() const
{
    return value_;
}

void LeafInt32::SetValue(int32_t value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

LeafInt64::LeafInt64(std::string path) : BaseNode(path)
{
}

int64_t LeafInt64::GetValue() const
{
    return value_;
}

void LeafInt64::SetValue(int64_t value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

LeafString::LeafString(std::string path) : BaseNode(path)
{
}

std::string LeafString::GetValue() const
{
    return value_;
}

void LeafString::SetValue(std::string value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

LeafUint8::LeafUint8(std::string path) : BaseNode(path)
{
}

uint8_t LeafUint8::GetValue() const
{
    return value_;
}

void LeafUint8::SetValue(uint8_t value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

LeafUint16::LeafUint16(std::string path) : BaseNode(path)
{
}

uint16_t LeafUint16::GetValue() const
{
    return value_;
}

void LeafUint16::SetValue(uint16_t value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

LeafUint32::LeafUint32(std::string path) : BaseNode(path)
{
}

uint32_t LeafUint32::GetValue() const
{
    return value_;
}

void LeafUint32::SetValue(uint32_t value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

LeafUint64::LeafUint64(std::string path) : BaseNode(path)
{
}

uint64_t LeafUint64::GetValue() const
{
    return value_;
}

void LeafUint64::SetValue(uint64_t value)
{
    value_ = value;
    SetPresence(true);
}


/**************************************************************************************************/

} /* Yang2Cpp */
