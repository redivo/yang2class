/**************************************************************************************************/

#include <string>

#ifndef __BASE_NODES_H__
#define __BASE_NODES_H__

namespace Yang2Cpp {

/**************************************************************************************************/
/**
 * \brief  Base node
 */
class BaseNode {
   public:
    /**
     * \brief  Constructor
     * \path   Path of node
     */
    BaseNode(std::string path);

    BaseNode() = delete;

    /**
     * \brief  Get Path
     * \return The node's path
     */
    const std::string& GetPath() const;

    /**
     * \brief  Inform if the node is present or not
     * \return TRUE if it's present, FALSE otherwise
     */
    bool IsPresent() const;

    /**
     * \brief  Set presence of node
     * \param  presence  TRUE means that the node is present, FALSE is the opposite
     */
    void SetPresence(bool presence);

   protected:
    std::string path_;
    bool is_present_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'boolean': "true" or "false"
 */
class LeafBoolean : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafBoolean(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    bool GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(bool value);

   private:
    bool value_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'decimal64': 64-bit signed decimal number
 */
class LeafDecimal64 : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafDecimal64(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    int64_t GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(int64_t value);

   private:
    int64_t value_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'empty': A leaf that does not have any value
 */
class LeafEmpty : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafEmpty(std::string path);
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'int8': 8-bit signed integer
 */
class LeafInt8 : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafInt8(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    int8_t GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(int8_t value);

   private:
    int8_t value_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'int16': 6-bit signed integer
 */
class LeafInt16 : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafInt16(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    int16_t GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(int16_t value);

   private:
    int16_t value_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'int32': 32-bit signed integer
 */
class LeafInt32 : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafInt32(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    int32_t GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(int32_t value);

   private:
    int32_t value_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'int64': 64-bit signed integer
 */
class LeafInt64 : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafInt64(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    int64_t GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(int64_t value);

   private:
    int64_t value_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'string': n-readable string
 */
class LeafString : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafString(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    std::string GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(std::string value);

   private:
    std::string value_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'uint8': 8-bit unsigned integer
 */
class LeafUint8 : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafUint8(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    uint8_t GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(uint8_t value);

   private:
    uint8_t value_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'uint16': 16-bit unsigned integer
 */
class LeafUint16 : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafUint16(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    uint16_t GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(uint16_t value);

   private:
    uint16_t value_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'uint32': 32-bit unsigned integer
 */
class LeafUint32 : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafUint32(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    uint32_t GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(uint32_t value);

   private:
    uint32_t value_;
};

/**************************************************************************************************/
/**
 * \brief  Leaf of type 'uint64': 64-bit unsigned integer
 */
class LeafUint64 : public BaseNode {
   public:
    /**
     * \brief  Constructor
     */
    LeafUint64(std::string path);

    /**
     * \brief  Get node value
     * \return Node value
     */
    uint64_t GetValue() const;

    /**
     * \brief  Set node value
     * \param  value  Value to be set
     */
    void SetValue(uint64_t value);

   private:
    uint64_t value_;
};

/**************************************************************************************************/

} /* Yang2Cpp */

#endif /* __BASE_NODES_H__ */
