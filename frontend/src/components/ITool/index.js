import {
    CodeSandboxOutlined,
    DiffOutlined,
    CopyOutlined,
    DeleteOutlined,
    BoldOutlined,
    FontSizeOutlined,
    FontColorsOutlined} from '@ant-design/icons';
import { Menu } from 'antd';
import React, { useState } from 'react';
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

const ITool = (props) => {
    const { abstract, setTitle } = props;
    const [current, setCurrent] = useState('infer');

    const onClick = (e) => {
        setCurrent(e.key);
        if (e.key === 'infer') {
            // post
            let postData = { 'abstract': abstract };
            fetch('http://127.0.0.1:8080/predict', {
                method: 'POST',
                mode: 'cors',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: JSON.stringify(postData)
            }).then(res => res.json()).then(res => {
                console.log(res['title'])
                setTitle(res['title'])
            });
        };
    };

    return (
        <Menu
            mode='inline'
            style={{
                height: '100%',
                borderRight: 0,
            }}
            onClick={ onClick }
            items={ items }
            selectable={ false }
        />
    );
};

export default ITool;
