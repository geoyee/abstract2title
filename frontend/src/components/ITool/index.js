import {
    CodeSandboxOutlined,
    DiffOutlined,
    CopyOutlined,
    DeleteOutlined,
    BoldOutlined,
    FontSizeOutlined,
    FontColorsOutlined} from '@ant-design/icons';
import { Menu } from 'antd';
import React from 'react';
import './index.css'

function getItem(label, key, icon) {
    return {
        label,
        key,
        icon,
    };
}

const items = [
    getItem('标题推理', 'infer', <CodeSandboxOutlined />),
    getItem('粘贴摘要', 'paste', <DiffOutlined />),
    getItem('清除摘要', 'delet', <DeleteOutlined />),
    getItem('复制标题', 'copy', <CopyOutlined />),
    getItem('字体加粗', 'bold', <BoldOutlined />),
    getItem('调整大小', 'size', <FontSizeOutlined />),
    getItem('调整颜色', 'color', <FontColorsOutlined />),
];  // submenu keys of first level

const ITool = () => {
    return (
        <Menu
            mode='inline'
            defaultSelectedKeys={['1']}
            style={{
                height: '100%',
                borderRight: 0,
            }}
            items={items}
        />
    );
};

export default ITool;
